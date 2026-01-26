from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from app.domain.services.user.customer import customer_service
from app.domain.services.user.user import user_service
from app.infrastructure.database.models.users import User

from .keyboards import main_menu


def get_create_owner_router() -> Router:
    router = Router()

    @router.message(Command(commands=["create_owner"]))
    async def create_owner(message: Message):
        from app.depends import provider

        async with provider.session_factory() as session:
            tg_user = message.from_user
            if not tg_user:
                await message.answer("⛔ Пользователь не найден")
                return

            user = await user_service.update_user_from_tlg(
                tlg_user=tg_user,
                bot_id=message.bot.id,
            )

            if not user:
                await message.answer("⛔ Ошибка при создании пользователя")
                return

            result = await session.execute(
                select(User.id).where(User.id == user.id),
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                from app.infrastructure.database.models.users import Customer

                owner_result = await session.execute(
                    select(Customer.id).where(Customer.owner_id == user.id),
                )
                existing_companies = owner_result.all()

                if existing_companies:
                    await message.answer(
                        "⚠️ Вы уже являетесь владельцем компании.\n"
                        "Используйте /start для доступа к админ-панели.",
                    )
                    return

            command_parts = message.text.split(maxsplit=1)
            if len(command_parts) < 2:
                await message.answer(
                    "❌ Неверный формат команды.\n"
                    "Использование: /create_owner <название_компании>\n"
                    "Пример: /create_owner Моя компания",
                )
                return

            company_name = command_parts[1].strip()

            if not company_name:
                await message.answer("❌ Название компании не может быть пустым")
                return

            try:
                customer = await customer_service.create_customer_with_admin_and_member(
                    current_user=user,
                    name=company_name,
                    session=session,
                )

                if customer:
                    await session.commit()
                    await message.answer(
                        f"✅ Компания '{company_name}' успешно создана!\n"
                        f"Вы назначены владельцем компании.\n"
                        f"ID компании: {customer.id}\n\n"
                        f"Теперь вы можете использовать /start для доступа к админ-панели.",
                    )
                else:
                    await message.answer("❌ Ошибка при создании компании")
            except Exception as e:
                await session.rollback()
                await message.answer(
                    f"❌ Произошла ошибка при создании компании: {e!s}",
                )

    return router


def get_admin_handlers_router() -> Router:
    router = Router()

    @router.message(Command(commands=["start", "menu"]))
    async def start_menu(
        message: Message, user: User | None = None, role: str | None = None
    ):
        if not user or role not in ("owner", "admin"):
            await message.answer("⛔ У вас нет доступа")
            return

        if role == "owner":
            header = "👑 Вы вошли как владелец"
        else:
            header = "🛠 Вы вошли как администратор"

        text = f"{header}\n\nДобро пожаловать в админ-панель!\nВыберите действие:"

        await message.answer(
            text=text,
            reply_markup=main_menu(),
        )

    return router
