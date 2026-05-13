[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

API для трекера привычек на основе книги **"Атомные привычки"** Джеймса Клира.

## 📋 Описание проекта

Проект представляет собой бэкенд-часть SPA веб-приложения для отслеживания полезных привычек. Пользователи могут создавать привычки, отмечать их выполнение и получать напоминания в Telegram.

### Основные возможности

- 🔐 **Аутентификация по email** с использованием JWT токенов
- 📝 **CRUD операции** для управления привычками
- 📄 **Пагинация** (5 привычек на страницу)
- 🌐 **Публичные привычки** для вдохновения
- 🤖 **Telegram бот** для отправки напоминаний
- ⏰ **Celery** для отложенных задач и периодических напоминаний
- 📚 **Документация API** (Swagger/ReDoc)

## 🛠 Технологии

- **Python** 3.11
- **Django** 4.2
- **Django REST Framework** 3.14
- **PostgreSQL** - база данных
- **Redis** - брокер для Celery
- **Celery** - отложенные задачи
- **JWT** - аутентификация
- **Telegram Bot API** - отправка уведомлений
- **Docker** / **Docker Compose** - контейнеризация

## 🚀 Установка и запуск

### Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Poetry (управление зависимостями)

## 1. Клонирование репозитория

git clone https://github.com/ваш-username/habit-tracker.git
cd habit-tracker

## Установка Poetry (если не установлен)
curl -sSL https://install.python-poetry.org | python3 -

## Установка зависимостей проекта
poetry install

## Копирование файла с примерами
cp .env.example .env

## Редактирование .env (укажите свои значения)
nano .env

### Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

### Database
DB_NAME=habit_tracker
DB_USER=habit_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

### Redis
REDIS_URL=redis://localhost:6379/0

### Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token

### CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

## Создание базы данных PostgreSQL
sudo -u postgres psql
CREATE DATABASE habit_tracker;
CREATE USER habit_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_user;
\q

### Применение миграций
poetry run python manage.py migrate

### Создание суперпользователя
poetry run python manage.py createsuperuser

## Терминал 1: Django сервер
poetry run python manage.py runserver

## Терминал 2: Celery worker
poetry run celery -A config worker --loglevel=info

## Терминал 3: Celery beat (периодические задачи)
poetry run celery -A config beat --loglevel=info

## 📚 Документация API

После запуска сервера документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **JSON Schema**: http://localhost:8000/api/schema/

### 🔑 Эндпоинты API

### Аутентификация

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/users/register/` | Регистрация пользователя |
| POST | `/api/users/token/` | Получение JWT токена |
| POST | `/api/users/token/refresh/` | Обновление токена |
| POST | `/api/users/token/verify/` | Проверка токена |
| GET | `/api/users/profile/` | Получение профиля |
| PUT | `/api/users/profile/` | Обновление профиля |
| POST | `/api/users/logout/` | Выход из системы |
| POST | `/api/users/check-email/` | Проверка email |

### Привычки

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/habits/` | Список привычек (пагинация 5) |
| POST | `/api/habits/` | Создание привычки |
| GET | `/api/habits/{id}/` | Детали привычки |
| PUT | `/api/habits/{id}/` | Полное обновление |
| PATCH | `/api/habits/{id}/` | Частичное обновление |
| DELETE | `/api/habits/{id}/` | Удаление привычки |
| GET | `/api/habits/public/` | Публичные привычки |

### Telegram

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/users/update-chat-id/` | Обновление Telegram chat_id |

## 🤖 Telegram Бот

Для получения напоминаний необходимо:

1. **Создать бота** через [@BotFather](https://t.me/BotFather)
2. **Получить токен** и добавить в `.env`
3. **Получить свой chat_id** через [@userinfobot](https://t.me/userinfobot)
4. **Сохранить chat_id** в профиле пользователя

## 🤖 Команды для управления ботом

### Отправка тестового сообщения
poetry run python manage.py send_test_message <chat_id> "Текст сообщения"

## 🧪 Тестирование

### Запуск всех тестов
poetry run python manage.py test

### Запуск с покрытием
poetry run coverage run --source='users,habits,telegram' manage.py test
poetry run coverage report

### Проверка качества кода
```text
poetry run flake8 .
poetry run black .
poetry run isort .
```

## 📁 Структура проекта

    habit-tracker/
    ├── config/                 # Настройки Django
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── celery.py
    │   └── wsgi.py
    ├── users/                  # Приложение пользователей
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   └── urls.py
    ├── habits/                 # Приложение привычек
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── validators.py
    │   ├── permissions.py
    │   └── urls.py
    ├── telegram/               # Приложение Telegram
    │   ├── models.py
    │   ├── tasks.py
    │   ├── utils.py
    │   └── management/
    │       └── commands/
    ├── tests/                  # Тесты
    │   ├── __init__.py
    │   ├── test_habits/
    │   ├── test_users/
    │   └── test_telegram/
    ├── pyproject.toml
    └── README.md

### 🔒 Безопасность
JWT токены с ограниченным временем жизни (15 минут)

CORS настроен для разрешенных доменов

Валидация всех входных данных

Переменные окружения для чувствительных данных

Права доступа: пользователи видят только свои привычки

### 🌐 Деплой

Проект развернут на удаленном сервере и доступен по адресу:
- **API**: http://31.184.253.113:80
- **Документация API**: http://31.184.253.113:80/api/docs/

### CI/CD
- Автоматические тесты при push в GitHub
- Автоматический деплой на сервер через GitHub Actions
- Docker контейнеризация приложения

### 👤 Автор
Алексей Ложкин

GitHub: @aleksey-s-lozhkin

### 🙏 Благодарности
Джеймс Клир за книгу "Атомные привычки"

Команда Django и DRF

Telegram Bot API