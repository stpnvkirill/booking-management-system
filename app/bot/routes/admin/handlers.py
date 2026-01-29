import base64

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.infrastructure.database.models.users import User

from .keyboards import main_menu


# TODO: не работают инсерты в БД, просто все виснет именно из бота  # noqa: TD002, TD003
def get_create_owner_router() -> Router:
    router = Router()

    async def token_answer(message: Message, user: User):
        binary_data = user.api_token.bytes
        token = base64.urlsafe_b64encode(binary_data).decode("utf-8").rstrip("=")
        response = (
            "🔐 **Ваш API токен:**\n\n"
            f'<span class="tg-spoiler">\n{token}\n</span>\n\n'
            "**Инструкции:**\n"
            "1. Используйте этот токен для авторизации в API\n"
            "2. Храните его в защищенном месте\n"  # noqa: RUF001
            "3. В случае компрометации немедленно сбросьте токен"  # noqa: RUF001
        )
        await message.answer(response, parse_mode="HTML")
        await message.delete()

    @router.message(Command(commands=["token"]))
    async def token(message: Message, user: User):
        await token_answer(message, user)

    """@router.message(Command(commands=["refresh_token"]))
    async def refresh_token(message: Message, user: User):
        new_user = await User.update(id=user.id, api_token=uuid.uuid4())
        await token_answer(message, new_user)"""

    """@router.message(Command(commands=["create_owner"]))
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

            owner_result = await session.execute(
                select(Customer.id).where(Customer.owner_id == user.id),
            )
            existing_companies = owner_result.all()

            if existing_companies:
                await message.answer(
                    "⚠️ Вы уже являетесь владельцем компании.\n"
                    "Используйте /menu для входа в админ-панель.",
                )
                return

            command_parts = message.text.split(maxsplit=1)
            if len(command_parts) < 2:
                await message.answer(
                    "❌ Неверный формат команды.\n"
                    "Использование:\n"
                    "/create_owner <название_компании>\n\n"
                    "Пример:\n"
                    "/create_owner Моя компания",
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
                await session.commit()

                await message.answer(
                    f"✅ Компания «{company_name}» успешно создана!\n"
                    f"Вы назначены владельцем.\n\n"
                    f"Теперь используйте /menu для входа в админ-панель.",
                )

            except Exception as e:
                await session.rollback()
                await message.answer(f"❌ Ошибка при создании компании: {e!s}")"""

    return router


def get_admin_handlers_router() -> Router:
    router = Router()

    @router.message(Command(commands=["start"]))
    async def start(message: Message):
        await message.answer(
            "👋 Добро пожаловать в админ-бот!\n"
            "Возможности админ-бота:\n"
            "• управление компаниями\n"
            "• управление заказчиками\n"
            "• добавление/удаление бота к заказчикам\n"
            "• назначение администраторов\n\n"
            "Команды:\n"
            "/create_owner — создать компанию\n"
            "/menu — открыть админ-панель",
        )

    @router.message(Command(commands=["menu"]))
    async def menu(
        message: Message,
        user: User | None = None,
        role: str | None = None,
    ):
        if not user or role not in ("owner", "admin"):
            await message.answer("⛔ У вас нет доступа")  # noqa: RUF001
            return

        header = (
            "👑 Вы вошли как владелец"
            if role == "owner"
            else "🛠 Вы вошли как администратор"
        )

        await message.answer(
            f"{header}\n\nДобро пожаловать в админ-панель!\nВыберите действие:",  # noqa: RUF001
            reply_markup=main_menu(),
        )

    return router
