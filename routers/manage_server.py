from typing import List
from fastapi import status, Depends, APIRouter
from database import database
from manage_server import repository, schemas
from jwt_token import jwt

router = APIRouter(
    prefix='/manage',
    tags=['ManageServer']
)

get_db = database.get_db


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.OutContactServerGet]
)
def get_all_manage_server(
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.get_all_manage_server(db)


@router.get(
    '/{name}/{_id}',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.OutContactServerGet]
    )
def get_manage_server(
    name: str,
    _id: int,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.get_manage_server(name, _id, db)


@router.post('/s', status_code=status.HTTP_201_CREATED)
def add_server_contacts(
    request: schemas.InServerInContacts,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.create_server_contacts(request, db)


@router.post('/u', status_code=status.HTTP_201_CREATED)
def add_contact_servers(
    request: schemas.InContactInServers,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.create_contact_servers(request, db)


@router.delete('/', status_code=status.HTTP_200_OK)
def delete_contact_server(
    request: schemas.INContactServerDelete,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository.delete_manage_server(request, db)
