FROM python:3.10.11

RUN pip install poetry

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY . .

RUN poetry install

WORKDIR /fastapi_app

RUN alembic upgrade head

CMD gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000