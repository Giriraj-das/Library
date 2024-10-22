### Warehouse
#### FastAPI, Alembic, SQLAlchemy(v2), Docker

To avoid downloading everything, you can run it in Docker.
In the `start` folder, rename `.env.example` to `.env`.
In the same directory, run `docker-compose up`.

#### or

- fork the repository
- `pip install poetry`
- `poetry install`
- `docker-compose up pg -d`
- from main.py run `run`
- or in terminal from `/src` run `uvicorn main:main_app --reload --host 127.0.0.1 --port 8000`