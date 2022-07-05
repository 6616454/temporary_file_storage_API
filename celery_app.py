from celery import Celery

from settings import settings

app = Celery(
    'service_tasks',
    broker=f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}',
    backend=f'redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}',
    include=['do_rar.tasks']
)

app.autodiscover_tasks()
