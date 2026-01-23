import os

from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI(title="BMS Alertserver")


class Alert(BaseModel):
    status: str
    labels: dict[str, str] = {}
    annotations: dict[str, str] = {}


class AlertManagerPayload(BaseModel):
    alerts: list[Alert] = []


def _telegram_url(token: str) -> str:
    return f"https://api.telegram.org/bot{token}/sendMessage"


def _format_alert(alert: Alert) -> str:
    name = alert.labels.get("alertname", "Unknown")
    severity = alert.labels.get("severity", "unknown")
    description = alert.annotations.get(
        "description",
        alert.annotations.get("summary", ""),
    )

    emoji = "🚨" if alert.status == "firing" else "✅"
    lines = [
        f"{emoji} ALERT",
        f"Name: {name}",
        f"Status: {alert.status}",
        f"Severity: {severity}",
    ]
    if description:
        lines.append(f"Description: {description}")
    return "\n".join(lines)


async def _send_telegram(token: str, chat_id: str, text: str) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            _telegram_url(token),
            data={"chat_id": chat_id, "text": text},
        )
        resp.raise_for_status()


async def _handle(data: AlertManagerPayload) -> dict:
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        raise HTTPException(status_code=500, detail="Telegram env vars not set")

    sent = 0
    for alert in data.alerts:
        await _send_telegram(token, chat_id, _format_alert(alert))
        sent += 1

    return {"status": "ok", "sent": sent}


@app.post("/alert")
async def alert_webhook_alert(data: AlertManagerPayload):
    return await _handle(data)
