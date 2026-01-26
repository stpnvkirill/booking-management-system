import random
import string
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy as sa

from app.depends import AsyncSession, provider


def generate_random_string(length=10):
    """
    Генерирует случайную строку заданной длины.
    """
    characters = string.ascii_letters + string.digits
    # Генерируем строку
    return "".join(random.choice(characters) for _ in range(length))  # noqa: S311


router = APIRouter(tags=["Health"])


@router.get(
    "/ping",
)
async def ping():
    return generate_random_string()


@router.get(
    "/ping-db",
)
async def ping_db(
    session: Annotated[AsyncSession, Depends(provider.get_session)],
):
    stmt = sa.text(
        "SELECT substring(md5(random()::text) from 1 for 10) as random_string;",
    )
    return await session.scalar(stmt)


@router.get(
    "/ping-error",
    summary="Test endpoint: returns 500 error",
    description="Используется для тестирования алерта High5xxErrorRate",
)
async def test_error_500():
    """Тестовый endpoint для генерации 500 ошибок."""
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Test 500 error for monitoring alerts",
    )
