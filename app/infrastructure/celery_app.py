from celery import Celery

celery_app = Celery(
    "booking_system",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# 🔥 ВАЖНО: автопоиск задач
celery_app.autodiscover_tasks(
    [
        "app.domain.services.feedback",
    ],
)

celery_app.conf.timezone = "UTC"
