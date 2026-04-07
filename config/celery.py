import os

from celery import Celery

# Устанавливаем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('habit_tracker')

# Загружаем настройки из Django settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Задача для отладки"""
    print(f'Request: {self.request!r}')
