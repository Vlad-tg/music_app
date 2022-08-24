from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_app.settings')

app = Celery('music_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Warsaw')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app.conf.beat_schedule = {
    'Send_mail_to_Client': {
        'task': 'core.tasks.send_mail_task',
        'schedule': 30.0, }
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
