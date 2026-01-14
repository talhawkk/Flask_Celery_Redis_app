from celery import Celery
from config import Config

def make_celery():
    celery=Celery(
        "worker",
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=["tasks"]
    )
    celery.conf.update(
        task_track_started=True,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",

    )
    return celery

celery= make_celery()