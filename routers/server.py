from fastapi import Depends, status
from database import database
from sqlalchemy.orm import Session
from fastapi import APIRouter
from server import schemas, repository
from jwt_token import jwt


router = APIRouter(
    tags=['Server'],
    prefix='/server'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_server(
    request: schemas.InServerSchemas,
    db: Session = Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):
    """ساخت سرور جدید"""

    return repository.create_server(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_servers(
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.get_servers(db)


@router.get('/{_id}', status_code=status.HTTP_200_OK)
def get_server(
    _id: int,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.get_server(_id, db)


@router.put('/{_id}', status_code=status.HTTP_200_OK)
def update_server(
    _id: int,
    request: schemas.InServerSchemas,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.update_server(_id, request, db)


@router.delete('/{_id}', status_code=status.HTTP_200_OK)
def delete_server(
    _id: int,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.delete_server(_id, db)
