import uuid as uuid_lib

from aiogram import types
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.config import config
from app.depends import AsyncSession, provider
from app.infrastructure.database.models.users import (
    BotConfig,
    Customer,
    CustomerAdmin,
    CustomerMember,
    User,
    UserBot,
)

from .customer import customer_service


class UserService:
    @provider.inject_session
    async def update_user_from_tlg(
        self,
        tlg_user: types.User,
        bot_id: int,
        session: AsyncSession = None,
    ) -> dict:
        kwargs = {
            "tlg_id": tlg_user.id,
            "first_name": tlg_user.first_name,
            "last_name": tlg_user.last_name,
            "username": tlg_user.username,
            "language_code": tlg_user.language_code,
        }
        stmt = (
            pg_insert(User)
            .values(
                kwargs,
            )
            .on_conflict_do_update(index_elements=["tlg_id"], set_=kwargs)
            .returning(User)
        )

        usr = await session.scalar(stmt)
        stmt_userbot = (
            pg_insert(UserBot)
            .values(
                {
                    "user_id": (
                        sa.select(User.id)
                        .where(User.tlg_id == tlg_user.id)
                        .scalar_subquery()
                    ),
                    "bot_id": bot_id,
                },
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt_userbot)

        if bot_id == config.bot.ADMINBOT_ID:
            return usr
        stmt_member = (
            pg_insert(CustomerMember)
            .values(
                {
                    "customer_id": (
                        sa.select(BotConfig.owner_id)
                        .where(BotConfig.id == bot_id)
                        .scalar_subquery()
                    ),
                    "user_id": (
                        sa.select(User.id)
                        .where(User.tlg_id == tlg_user.id)
                        .scalar_subquery()
                    ),
                },
            )
            .on_conflict_do_nothing()
        )
        await session.execute(stmt_member)
        return usr

    @provider.inject_session
    async def get_if_available(
        self,
        current_user_id: uuid_lib.UUID,
        user_id: uuid_lib.UUID,
        session: AsyncSession | None = None,
    ) -> User | None:
        exist_customers = (
            sa.select(CustomerMember.customer_id)
            .select_from(CustomerAdmin)
            .join(Customer, Customer.id == CustomerAdmin.customer_id)
            .where(
                sa.or_(
                    CustomerAdmin.user_id == current_user_id,
                    Customer.owner_id == current_user_id,
                ),
            )
            .subquery()
        )
        exist_users = (
            sa.select(CustomerMember.user_id)
            .where(CustomerMember.customer_id.in_(exist_customers))
            .subquery()
        )

        stmt = sa.select(User).where(
            User.id == user_id,
            User.id.in_(exist_users),
        )
        return await session.scalar(stmt)

    @provider.inject_session
    async def user_can_add_bot(
        self,
        user_id: uuid_lib.UUID,
        customer_id: uuid_lib.UUID,
        session: AsyncSession | None = None,
    ) -> bool:
        stmt = (
            sa.select(sa.func.count(CustomerAdmin.customer_id) > 0)
            .select_from(CustomerAdmin)
            .where(
                CustomerAdmin.customer_id == customer_id,
                CustomerAdmin.user_id == user_id,
            )
        )
        return await session.scalar(stmt)

    @provider.inject_session
    async def create_test_user(
        self,
        session: AsyncSession | None = None,
    ) -> User:
        if not config.bot.CREATE_TEST_USER:
            return None
        if test_user := await User.get(
            id=uuid_lib.UUID("e35b77b7-1cf9-4c75-8e2b-c491b53620ae"),
            session=session,
        ):
            await User.update(
                id=uuid_lib.UUID("e35b77b7-1cf9-4c75-8e2b-c491b53620ae"),
                tlg_id=config.bot.TEST_USER_TLG_ID,
                session=session,
            )
            return None
        test_user = await User.create(
            id=uuid_lib.UUID("e35b77b7-1cf9-4c75-8e2b-c491b53620ae"),
            api_token=uuid_lib.UUID("019bab3e-606d-7e4e-b253-7959fce99ff4"),
            tlg_id=config.bot.TEST_USER_TLG_ID,
            first_name="Test",
            last_name="User",
            username="testuser",
            language_code="ru",
            session=session,
        )
        await customer_service.create_customer_with_admin_and_member(
            current_user=test_user,
            name="Test Customer",
            session=session,
        )


user_service = UserService()
