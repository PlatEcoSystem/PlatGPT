FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и ставим их
COPY dev/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Запуск бота из папки dev
CMD ["python", "dev/main.py"]