from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from views import router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    title='Warehouse',
    description='FastAPI, PostgreSQL, SQLAlchemy(v2), Docker, Pytest',
)
main_app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
