import logging
import os

from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI(title="BMS Alertserver")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alertserver")


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

    if alert.status == "firing":
        emoji = "🚨"
        description = alert.annotations.get(
            "description",
            alert.annotations.get("summary", ""),
        )
    else:
        emoji = "✅"
        description = alert.annotations.get(
            "resolved_description",
            f"Сервис {name} вернулся в норму ✅",
        )

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
        try:
            resp = await client.post(
                _telegram_url(token),
                data={"chat_id": chat_id, "text": text},
            )

            if resp.status_code >= httpx.codes.BAD_REQUEST:
                logger.error(
                    "Telegram API error %s: %s",
                    resp.status_code,
                    resp.text,
                )
                return

        except httpx.RequestError as e:
            logger.exception("Telegram request failed: %s", e)
            return


@app.post("/alert")
async def alert_webhook(data: AlertManagerPayload):
    token = os.getenv("TG_BOT_ALERT_TOKEN")
    chat_id = os.getenv("TG_ALERT_CHAT_ID")

    if not token or not chat_id:
        raise HTTPException(
            status_code=500,
            detail="Telegram env vars TG_BOT_ALERT_TOKEN / TG_ALERT_CHAT_ID not set",
        )

    sent = 0

    for alert in data.alerts:
        await _send_telegram(token, chat_id, _format_alert(alert))
        sent += 1

    return {
        "status": "ok",
        "received": len(data.alerts),
        "processed": sent,
    }
