# Coworking Space Booking System

Современное веб-приложение для управления бронированием мест в коворкингах, сделанное с использованием Flask (backend) и React (frontend)

## Features

- Быстро. Минимизировано количество шагов в процессе бронирования
- Гарантированно. Обеспечивает актуальное отображение свободных мест и возможность узнать загруженность на нужные дату/время
- Не допускает возможности брони одного места двумя участниками
- Удобно. Интуитивно понятный интерфейс без лишних переходов, с линейной навигацией по сценариям использования
- Есть редактирование и удаление бронирования
- Функция редактирования данных профиля

## Tech Stack

### Backend
- Python 3.9+
- Flask
- PostgreSQL
- SQLAlchemy
- Flask-RESTX (for Swagger)
- Pytest

### Frontend
- React
- Material-UI
- React Query

### Infrastructure
- Docker
- Docker Compose
- GitHub Actions (CI)

## Project Structure

```
.
├── backend/                 # Flask backend
│   ├── app/                # Application code
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── package.json       # Node dependencies
└── docker/                # Docker configuration
    ├── backend/          # Backend Dockerfile
    ├── frontend/         # Frontend Dockerfile
    └── docker-compose.yml # Docker Compose configuration
```

Docker Compose:
```
docker-compose down && docker-compose up --build -d

docker-compose down 
docker-compose build backend
docker-compose up --build

# Запуск тестов с пересборкой докера
docker-compose down backend && docker-compose up --build -d backend && docker-compose run --rm test

```

## Development

### Frontend Development, Backend Development 

Отладка через Docker контейнер
Локальный порт backend: 5678
Chrome локальный порт frontend: 9222

## Testing

### Backend Tests
```shell
docker-compose run --rm test
```

## Доступы к проекту

Frontend: http://localhost:3000
Backend API: http://localhost:5000
PgAdmin (для управления базой данных): http://localhost:5050

# Swagger docs

Путь: http://localhost:5000/api/docs

# Запуск приложения

1. Через pgAdmin создать базу данных coworking ( http://localhost:5050/browser/ )
2. В докере перейти в командную строку backend приложения и выполнить миграции командой:
    flask db upgrade
3. После применения миграций в базе данных появится информация:
    4 рабочих пространства, 
    2 пользователя (один из них person@example.com : admin123)

## Установка

1. **Клонировать репозиторий:**
   ```sh
   git clone -b devc https://git.culab.ru/course-projects/fundamentals-of-industrial-programming-2025/course-project/a.kashirina.git
   ```
   Клонировать конкретную ветку (название ветки заменить на актуальное)
2. **Перейти в папку проекта**
   ```sh
   cd a.kashirina
   ```
3. **Создать докер контейнеры:**
   ```sh
   docker-compose up --build -d
   ```
4. **Применить миграции:**
   ```sh
    docker-compose run backend flask db upgrade
   ```
5. **Войти в debug режим(зависит от редактора):**
    Приложение работает, но возникает непонятная ошибка, которая решается только вхождением в debug режим
6. **Запустить приложение:**
    http://localhost:3000
