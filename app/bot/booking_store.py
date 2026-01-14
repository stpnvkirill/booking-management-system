import asyncio
import uuid
from datetime import datetime
from typing import Any

from app.log import log


class BookingStore:
    """Простой in-memory сторедж броней (для прототипа).

    В реальном приложении будет заменён на работу с БД.
    """

    def __init__(self):
        self._store: dict[int, list[dict[str, Any]]] = {}

    def _ensure_user(self, user_id: int) -> list[dict[str, Any]]:
        return self._store.setdefault(user_id, [])

    def add_booking(self, user_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        booking = {
            "id": str(uuid.uuid4()),
            "status": "pending",
            "created_at": datetime.utcnow(),
            **payload,
        }
        self._ensure_user(user_id).append(booking)
        return booking

    def list_bookings(self, user_id: int) -> list[dict[str, Any]]:
        return list(self._store.get(user_id, []))

    def set_status(self, user_id: int, booking_id: str, status: str) -> dict[str, Any] | None:
        bookings = self._store.get(user_id, [])
        for b in bookings:
            if b["id"] == booking_id:
                b["status"] = status
                b["updated_at"] = datetime.utcnow()
                return b
        return None


store = BookingStore()


def format_booking(booking: dict[str, Any]) -> str:
    "Человекочитаемое описание брони."
    return (
        f"Бронь #{booking['id']}\n"
        f"Тип: {booking['resource_type']}\n"
        f"Ресурс: {booking['resource']}\n"
        f"Дата: {booking['date']}\n"
        f"Время: {booking['time']}\n"
        f"Статус: {booking['status']}"
    )


async def auto_confirm(user_id: int, booking_id: str, delay_sec: int, notify):
    "Имитация фонового подтверждения с уведомлением."
    await asyncio.sleep(delay_sec)
    updated = store.set_status(user_id, booking_id, "confirmed")
    if updated:
        await notify(updated)
        log(
            level="info",
            method="auto_confirm",
            path="booking_store",
            text_detail=f"Booking {booking_id} auto-confirmed",
            user_id=user_id,
        )


