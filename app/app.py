import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.depends import provider
from app.domain.services.feedback import feedback_service
from app.domain.services.notification.service import NotificationService
from app.schedulers.scheduler import NotificationScheduler

from .api import routes
from .bot import bot_manager
from .domain.services import user_service
from .middlewares import LoggingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

for logger_name in [
    "aiogram",
    "aiogram.event",
    "aiogram.dispatcher",
    "httpx",
    "apscheduler",
]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_application() -> FastAPI:
    from .config import config  # noqa: PLC0415

    swagger_url = None
    openapi_url = None
    redoc_url = None

    notification_service = NotificationService(provider.session_factory)
    scheduler = NotificationScheduler(
        provider.session_factory,
        notification_service,
        feedback_service,
    )

    if config.server.SWAGGER_ENABLE:
        swagger_url = "/docs"
        openapi_url = "/openapi.json"

    application = FastAPI(
        title=config.server.SERVER_NAME,
        description=config.server.SERVER_DESCRIPTION,
        debug=config.server.DEBUG,
        version=config.server.API_VERSION,
        docs_url=swagger_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
        responses=config.server.server_responces,
        swagger_ui_parameters=config.server.swagger_ui_parameters,
        on_startup=[
            bot_manager.run_all,
            user_service.create_test_user,
            scheduler.start,
        ],
        on_shutdown=[
            bot_manager.stop_all,
            scheduler.stop,
        ],
    )

    application.middleware("http")(LoggingMiddleware())
    for route in routes:
        application.include_router(route, prefix="/api")

    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=False,
    ).instrument(application).expose(application, include_in_schema=False)

    return application
