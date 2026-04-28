echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# создание test database
PGPASSWORD=postgres psql -h db -U postgres -c "DROP DATABASE IF EXISTS coworking_test;"
PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE coworking_test;"

# применение миграций с помощью Python
echo "Applying migrations..."
python << END
from flask import Flask
from flask_migrate import Migrate, upgrade
from app import create_app, db
from config import TestConfig

app = create_app(TestConfig)
with app.app_context():
    upgrade()
END

# запуск тестов
echo "Running tests..."
python -m pytest tests/ -v 