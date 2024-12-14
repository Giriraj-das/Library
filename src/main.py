from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from author import router as author_router
from book import router as book_router
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    title='Library',
    description='API for working with books, authors, and issuing books to readers. '
                'FastAPI, PostgreSQL, SQLAlchemy(v2), Docker, Pytest',
)
main_app.include_router(author_router)
main_app.include_router(book_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:main_app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
