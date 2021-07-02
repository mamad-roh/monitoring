from fastapi import status, Depends, APIRouter
from database import database
from manage_server import repository, schemas

router = APIRouter(
    prefix='/manage',
    tags=['ManageServer']
)

get_db = database.get_db


@router.post('/s', status_code=status.HTTP_201_CREATED)
def add_server_contacts(
    request: schemas.InServerInContacts,
    db=Depends(get_db)
):

    return repository.create_server_contacts(request, db)


@router.post('/u', status_code=status.HTTP_201_CREATED)
def add_contact_servers(
    request: schemas.InContactInServers,
    db=Depends(get_db)
):

    return repository.create_contact_servers(request, db)
