### Warehouse
#### FastAPI, Alembic, SQLAlchemy(v2), Docker

Чтобы все не скачивать, можно запустить в Докере.
В папке `start` переименовать `.env.example` на `.env`.
В этой же директории выполнить `docker-compose up`.

#### или

- сделать форк
- `pip install poetry`
- `poetry install`
- `docker-compose up pg -d`
- из main.py запустить `run`
- или в терминале из `src` запустить `uvicorn main:main_app --reload --host 127.0.0.1 --port 8000`