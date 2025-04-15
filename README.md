# Task API

## Установка и запуск

1. Клонируй репозиторий: git clone https://github.com/MrSidAlex/FAT.git
2. Установи зависимости: poetry install
3. Обнови зависимости: poetry update
4. Запусти проект: docker-compose up --build


## Эндпоинты

- `GET /tasks/` — получить список задач (с фильтрами по статусу и дедлайну)
- `GET /tasks/{task_id}` — получить задачу по ID
- `POST /tasks` — создать новую задачу
- `PUT /tasks/{task_id}` — обновить задачу по ID
- `DELETE /tasks/{task_id}` — удалить задачу по ID

## Стек технологий

- **FastAPI** — быстрый и современный веб-фреймворк для создания API
- **SQLAlchemy 2.0 (async)** — асинхронная работа с базой данных через ORM
- **asyncpg** — асинхронный драйвер для PostgreSQL
- **Pydantic** — валидация данных
- **Poetry** — управление зависимостями и окружением
- **Uvicorn** — ASGI-сервер для запуска FastAPI
- **dotenv** — загрузка переменных окружения из `.env`
- **async/await** — асинхронное выполнение запросов и взаимодействие с БД
- **Docker + Docker Compose** — контейнеризация и запуск проекта
