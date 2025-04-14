import logging
from fastapi import status
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from datetime import datetime
from typing import List, Optional


from base_db import async_session_maker
from models import Task, TaskBase

app = FastAPI()

# Логгер для приложения
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Утилита для парсинга task row в dict
def serialize_task(task_row) -> dict:
    return {
        "id": task_row[0],
        "title": task_row[1],
        "description": task_row[2],
        "deadline": task_row[4],
        "status": task_row[5],
        "created_at": task_row[3],
    }


CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);
"""


@app.get("/tasks/", response_model=List[Task])
async def get_tasks(
        status: Optional[str] = None,
        deadline: Optional[datetime] = None,
):
    """
    Получение задач с фильтрами по статусу и дедлайну.
    Если фильтры не указаны, возвращаются все задачи.
    """
    filters = []
    query = "SELECT * FROM tasks"

    # Добавляем фильтр по статусу, если он задан
    if status:
        filters.append(f"status = '{status}'")

    # Добавляем фильтр по дедлайну, если он задан
    if deadline:
        filters.append(f"deadline <= '{deadline}'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    logger.info(f"Executing query: {query}")

    try:
        async with async_session_maker() as session:
            result = await session.execute(text(query))
            tasks = result.all()
            return [serialize_task(task) for task in tasks]
    except Exception as e:
        logger.error(f"Ошибка получения задач.: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при получении задач.",
        )


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """
    Получение задачи по ID.
    """
    query = text("SELECT * FROM tasks WHERE id = :task_id")
    try:
        async with async_session_maker() as session:
            result = await session.execute(query, {"task_id": task_id})
            task = result.first()

            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

            return serialize_task(task)

    except Exception as e:
        logger.error(f"Ошибка получения задачи по id {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при получении задачи",
        )


@app.post("/tasks", response_model=TaskBase, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskBase):
    """
    Создание новой задачи.
    """
    query = text("""
        INSERT INTO tasks (title, description, deadline, status)
        VALUES (:title, :description, :deadline, :status)
        RETURNING id, title, description, deadline, status, created_at;
    """)

    try:
        async with async_session_maker() as session:
            result = await session.execute(query, task.dict())
            new_task = result.first()
            await session.commit()

            if not new_task:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Не удалось создать задачу")

            return TaskBase(**dict(new_task._mapping))

    except Exception as e:
        logger.error(f"Ошибка создания задачи: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при создании задачи.",
        )


@app.put("/tasks/{task_id}", response_model=TaskBase)
async def update_task(task_id: int, task: TaskBase):
    """
    Обновление задачи по ID.
    """
    query = text("""
        UPDATE tasks
        SET title = :title,
            description = :description,
            deadline = :deadline,
            status = :status
        WHERE id = :task_id
        RETURNING id, title, description, deadline, status, created_at;
    """)

    try:
        params = {**task.dict(), "task_id": task_id}
        async with async_session_maker() as session:
            result = await session.execute(query, params)
            updated_task = result.first()
            await session.commit()

            if not updated_task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена.")

            return TaskBase(**dict(updated_task._mapping))

    except Exception as e:
        logger.error(f"Ошибка изменения задачи по id {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при обновлении задачи.",
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """
    Удаление задачи по id.
    """
    query = text("""
        DELETE FROM tasks
        WHERE id = :task_id
        RETURNING id;
    """)

    try:
        async with async_session_maker() as session:
            result = await session.execute(query, {"task_id": task_id})
            deleted_task = result.first()
            await session.commit()

            if not deleted_task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена.")

            return {"detail": "Задача удалена успешно."}

    except Exception as e:
        logger.error(f"Ошибка удаления задачи с id {task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при удалении задачи.",
        )
