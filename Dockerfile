FROM python:3.12
WORKDIR /app

COPY app/ /app/
COPY app/pyproject.toml app/poetry.lock* /app/
RUN pip install -U --pre pip poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

CMD ["sh", "-c", "python /app/init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
