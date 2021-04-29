from celery.schedules import crontab

from .settings import app

app.conf.beat_schedule = {
    'download_meme': {
        'task': 'parsers.tasks.download_memes',
        'schedule': 60 * 10,  # Every 1 hour
        'args': [30],
    }
}

app.autodiscover_tasks()
