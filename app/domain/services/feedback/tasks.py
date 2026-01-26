from app.infrastructure.celery_app import celery_app


@celery_app.task
def review_reminder_task():
    pass
