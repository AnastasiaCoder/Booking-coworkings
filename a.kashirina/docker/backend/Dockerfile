FROM python:3.9-slim

WORKDIR /app

# установка системных зависимостей
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app
# ENV FLASK_ENV=production
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000 5678

# использование debugpy для отладки
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"] 