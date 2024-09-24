FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.8.3
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root --no-dev

COPY src/ .

EXPOSE 8000

CMD alembic upgrade head && uvicorn main:main_app --host 0.0.0.0 --port 8000 --workers 4
