from celery import Celery
from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

settings = get_settings()

celery = Celery(
    "fastapi-ca",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    broker_connection_retry_on_startup=True,
    include=["example.ch10_02.celery_task"],
)

celery.register_task(SendWelcomeEmailTask())