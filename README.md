
# Habit Tracker 

Приложение для формирования полезных привычек с интеграцией Telegram-бота (только оповещения).  
**Стек**: Django, DRF, PostgreSQL, Docker, Celery, Redis

## Технические требования
- Docker 20.10+
- Docker Compose 2.5+
- Python 3.13 (в контейнере)

## Быстрый старт с Docker

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/Chocoeater/Habit-Tracker.git
   cd Habit-Tracker
   ```

2. **Настройте окружение**:
   - Создайте `.env` файл (на основе `.env.example`):
     ```bash
     cp .env.example .env
     ```
   - Обновите секретные ключи:
     ```env
     SECRET_KEY=ваш_секретный_ключ
     TELEGRAM_BOT_TOKEN=ваш_токен_бота
     ```

3. **Запустите сервисы**:
   ```bash
   docker-compose up -d --build
   ```

5. **Создайте суперпользователя**:
   ```bash
   docker-compose exec web python manage.py create_admin
   ```

## Доступ к сервисам
- **Django-приложение**: http://localhost:8000
- **Админка**: http://localhost:8000/admin
- **Документация API**: http://localhost:8000/redoc/


