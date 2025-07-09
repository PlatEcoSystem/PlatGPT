FROM python:3.11-slim

WORKDIR /app

COPY dev/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dev/ ./dev/

CMD ["python", "dev/main.py"]
