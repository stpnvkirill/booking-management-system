"""
API эндпоинты для работы с комнатами (переговорными).

Структура файлов:
- create.py  - POST   /api/rooms       - создание комнаты
- read.py    - GET    /api/rooms/{id}  - получение данных о комнате
- update.py  - PUT    /api/rooms/{id}  - обновление данных о комнате
- delete.py  - DELETE /api/rooms/{id}  - удаление комнаты
"""
from fastapi import APIRouter

from .create import router as create_router
from .read import router as read_router
from .update import router as update_router
from .delete import router as delete_router

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# Подключаем все роутеры
router.include_router(create_router)
router.include_router(read_router)
router.include_router(update_router)
router.include_router(delete_router)
