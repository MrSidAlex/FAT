from base_db import async_session_maker
import asyncio
from sqlalchemy import text


async def create_table_if_not_exists():
    try:
        async with async_session_maker() as session:
            # Попробуем создать таблицу
            await session.execute(text("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    deadline DATE NOT NULL,
                    status TEXT NOT NULL
                )
            """))
            await session.commit()
            print("Table created successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


asyncio.run(create_table_if_not_exists())
