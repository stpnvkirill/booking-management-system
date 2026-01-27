from collections.abc import Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.infrastructure.database.models import (
    Customer,
    CustomerAdmin,
)


class RoleCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message | CallbackQuery,
        data: dict,
    ):
        if (
            isinstance(event, Message)
            and event.text
            and event.text.startswith("/start")
        ):
            return await handler(event, data)

        session: AsyncSession = data.get("session")
        if not session:
            await self._deny_access(event, "⛔ Ошибка доступа к базе данных")
            return None

        user = data.get("user")
        if not user:
            await self._deny_access(event, "⛔ У вас нет доступа")  # noqa: RUF001
            return None

        owner_result = await session.execute(
            select(Customer.id).where(Customer.owner_id == user.id),
        )
        owner_customer_ids = [row[0] for row in owner_result.all()]

        admin_result = await session.execute(
            select(CustomerAdmin.customer_id).where(
                CustomerAdmin.user_id == user.id,
            ),
        )
        admin_customer_ids = [row[0] for row in admin_result.all()]

        if not owner_customer_ids and not admin_customer_ids:
            await self._deny_access(event, "⛔ У вас нет доступа")  # noqa: RUF001
            return None

        data["role"] = "owner" if owner_customer_ids else "admin"
        data["customer_ids"] = set(owner_customer_ids + admin_customer_ids)

        return await handler(event, data)

    async def _deny_access(
        self,
        event: Message | CallbackQuery,
        message: str,
    ):
        try:
            if isinstance(event, CallbackQuery):
                await event.answer(message, show_alert=True)
            elif isinstance(event, Message):
                await event.answer(message)
        except Exception:  # noqa: BLE001, S110
            pass
