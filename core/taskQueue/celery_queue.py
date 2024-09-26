import os

from celery import Celery


def configure_celery() -> Celery:
    celery_app = Celery('tasks', broker=f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0")
    celery_app.conf.result_backend = f'db+postgresql://{os.getenv("CELERY_DB_USER")}:{os.getenv("CELERY_DB_PASS")}@\
    {os.getenv("CELERY_DB_HOST")}/{os.getenv("CELERY_DB_NAME")}'
    return celery_app
