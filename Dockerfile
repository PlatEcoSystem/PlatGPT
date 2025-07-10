FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt из dev/
COPY dev/requirements.txt ./requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (включая dev/ и data-prep/)
COPY . .

# Запускаем бота
CMD ["python", "dev/main.py"]
