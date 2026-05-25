FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "-c", "import os; from uvicorn import run; run('main:app', host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))"]
