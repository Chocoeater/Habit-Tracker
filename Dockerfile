FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

# Копируем весь проект
COPY . .

ENV CELERY_RESULT_BACKEND = "redis://redis:6379/0"
ENV CELERY_BROKER_URL = "redis://redis:6379/1"

# Запускаем приложение
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]