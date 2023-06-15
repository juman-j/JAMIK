FROM python:3.10.11

RUN pip install poetry

RUN mkdir /app

WORKDIR /app

COPY . .

RUN poetry install

WORKDIR /app

RUN poetry run alembic upgrade head

EXPOSE 8000

CMD poetry run gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000