from fastapi import Depends, status
from database import database
from sqlalchemy.orm import Session
from fastapi import APIRouter
from server import schemas, repository


router = APIRouter(
    tags=['Server'],
    prefix='/server'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_server(
    request: schemas.InServerSchemas,
    db: Session = Depends(get_db)
):
    """ساخت سرور جدید"""

    return repository.create_server(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_servers(db=Depends(get_db)):

    return repository.get_servers(db)


@router.get('/{_id}', status_code=status.HTTP_200_OK)
def get_server(_id: int, db=Depends(get_db)):

    return repository.get_server(_id, db)


@router.put('/{_id}', status_code=status.HTTP_200_OK)
def update_server(
    _id: int,
    request: schemas.InServerSchemas,
    db=Depends(get_db)
):

    return repository.update_server(_id, request, db)


@router.delete('/{_id}')
def delete_server(_id: int, db=Depends(get_db)):

    return repository.delete_server(_id, db)
