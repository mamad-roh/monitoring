from database import database
from fastapi import APIRouter, status, Depends
from media import schemas, repository

router = APIRouter(
    tags=['Media'],
    prefix='/media'
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_media(
    request: schemas.InMediaSchemas,
    db=Depends(get_db)
):
    """ساخت مدیا جدید"""

    return repository.create_media(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_all_media(db=Depends(get_db)):
    """برشگت تمام مدیا"""

    return repository.get_all_media(db)


@router.get('/{_id}', status_code=status.HTTP_200_OK)
def get_media(_id: int, db=Depends(get_db)):
    """برگشت یک مدیا"""

    return repository.get_media(_id, db)


@router.put('/{_id}', status_code=status.HTTP_200_OK)
def update_media(
    _id: int,
    request: schemas.InMediaSchemasUpdate,
    db=Depends(get_db)
):
    """آپدیت یک مدیا در صورت وجود"""

    return repository.update_media(_id, request, db)


@router.delete('/{_id}', status_code=status.HTTP_200_OK)
def delete_media(_id: int, db=Depends(get_db)):
    """دلیت کردن مدیا در صورت وجود"""

    return repository.delete_media(_id, db)
