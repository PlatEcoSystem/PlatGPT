FROM python:3.11-slim

WORKDIR /app

COPY dev/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем dev
COPY dev ./dev

# 🔥 Копируем папку с фотками
COPY photos ./dev/photos

COPY data-prep ./data-prep

CMD ["python", "dev/main.py"]