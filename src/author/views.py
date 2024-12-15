from fastapi import APIRouter, Depends, status

from author.schemas import AuthorSchema, AuthorsSchema
from author import services
from core.config import settings
from core.models import Author

router = APIRouter(prefix=settings.prefix.author, tags=['Authors'])


@router.post('', response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
async def create_author(author: Author = Depends(services.create_author)):
    return author


@router.get('', response_model=list[AuthorsSchema])
async def get_authors(authors: list[Author] = Depends(services.get_authors)):
    return authors


@router.get('/{author_id}', response_model=AuthorSchema)
async def get_author(author: Author = Depends(services.get_author)):
    return author


@router.put('/{author_id}', response_model=AuthorSchema)
async def update_author(author: Author = Depends(services.update_author)):
    return author


@router.delete(
    '/{author_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(services.delete_author)]
)
async def delete_author() -> None:
    pass
