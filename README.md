
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

## Доступ к сервисам (Локально)
- **Django-приложение**: http://localhost:8000
- **Админка**: http://localhost:8000/admin
- **Документация API**: http://localhost:8000/redoc/


# Инструкция по ручному деплою на сервер
Подготовка сервера (Ubuntu 20.04/22.04)
1. Обновление системы и установка базовых пакетов
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git python3-pip python3-venv
```
2. Установка Docker и Docker Compose
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```
3. Настройка firewall
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```
# Ручной деплой приложения
1. Клонирование проекта
```bash
cd ~
git clone -b develop https://github.com/Chocoeater/Habit-Tracker.git
cd Habit-Tracker
```
2. Создание файла окружения
```bash
cp .env.example .env
nano .env
```
Заполните .env файл в соответствии с файлом .env.example

3. Генерация SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
4. Запуск приложения
```bash
# Сборка и запуск контейнеров
docker-compose -f docker-compose.prod.yml up -d --build

# Или если используете стандартный docker-compose.yml
docker-compose up -d --build
```
5. Выполнение миграций
```bash
docker-compose exec web python manage.py migrate
```
6. Создание суперпользователя
```bash
docker-compose exec web python manage.py create_admin
```

# CI/CD

Перейдите в Settings → Secrets and variables → Actions и добавьте:

Secrets:

DOCKERHUB_USERNAME - ваш Docker Hub логин

DOCKERHUB_ACCESS_TOKEN - Docker Hub Personal Access Token

SSH_PRIVATE_KEY - приватный SSH ключ для сервера

SERVER_IP - IP адрес сервера

SSH_USERNAME - пользователь для SSH (обычно root или ubuntu)

### Пример файла для тестирования и деплоя на сервер через workflow:
```yml
name: Django CI

on: [ push, pull_request ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry config virtualenvs.create false
          poetry install --no-interaction --no-root

      - name: Run migrations
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DATABASE_URL: sqlite:///db.sqlite3
          DEBUG: False
        run: |
          python manage.py migrate

      - name: Run tests
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DATABASE_URL: sqlite:///db.sqlite3
          DEBUG: False
        run: |
          python manage.py test

  build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        run: echo ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }} | docker login -u ${{ secrets.DOCKER_HUB_USERNAME }} --password-stdin

      - name: Build Docker image
        run: docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }} .

      - name: Push Docker image to Docker Hub
        run: docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}

      - name: Deploy to server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            cd Habit-Tracker
  
            
            sed -i \"s|image: chocoeater/myapp:latest|image: chocoeater/myapp:${{ github.sha }}|\" docker-compose.yml
  
            
            docker-compose down 
            docker-compose up -d 
  
           
            docker-compose ps
            echo "Deployment completed!"
          "
```
