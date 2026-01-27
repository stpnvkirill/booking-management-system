from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import config


class Provider:
    def __init__(self):
        self.engine = create_async_engine(
            url=config.database.database_url,
            echo=config.database.DB_ECHO,
            pool_size=30,
            max_overflow=15,
            pool_timeout=15.0,
            pool_recycle=3600,
            pool_pre_ping=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self._current_user = None

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as err:
                await session.rollback()
                raise err
            finally:
                await session.close()

    def inject_session(self, func):
        async def wrapper(*args, **kwargs):
            # Создаем новую сессию только если она не передана или равна None
            if "session" not in kwargs or kwargs.get("session") is None:
                async with self.session_factory() as session:
                    kwargs["session"] = session
                    try:
                        res = await func(*args, **kwargs)
                        await session.commit()
                    except Exception as err:
                        await session.rollback()
                        raise err
                    return res

            return await func(*args, **kwargs)

        return wrapper

    def set_current_user(self, user):
        self._current_user = user

    @property
    def current_user(self):
        return self._current_user


provider = Provider()
