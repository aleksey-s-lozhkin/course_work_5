from .settings import *  # noqa: F401, F403


# Принудительно используем SQLite для CI
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test_db.sqlite3',
    }
}

# Отключаем брокеры для CI
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'cache'

# Упрощаем для CI
DEBUG = True
SECRET_KEY = 'ci-test-secret-key'
