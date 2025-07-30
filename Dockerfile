
# Используем официальный python-образ как базовый
FROM python:3.11-slim

# Устанавливаем зависимости для сборки Python пакетов и работы с PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем requirements.txt отдельно для кэширования слоёв
COPY requirements.txt .

# Устанавливаем зависимости python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект в контейнер
COPY . .

# Собираем статические файлы (можно закомментировать, если собираете их из docker-compose)
# RUN python manage.py collectstatic --noinput

# Открываем порт для gunicorn/django
EXPOSE 8000

# Значение по умолчанию (можно переопределить командой в docker-compose.yaml)
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn stripe_test.wsgi:application --bind 0.0.0.0:8000"]
