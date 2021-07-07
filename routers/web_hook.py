from fastapi import status, APIRouter, Depends, Request
from web_hook import schemas, repository_v2, repository_token
from database import database

router = APIRouter(
    tags=['WebHook'],
    prefix='/web_hook'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_200_OK)
def send_notif(
    request: schemas.InWebHookSchemas,
    a: Request,
    db=Depends(get_db)
):
    print(request.message)
    print(a.client.host)
    return repository_v2.receive_post(request, db)


@router.post('/token', status_code=status.HTTP_200_OK)
def create_token(
    request: schemas.InTokenSchemas,
    db=Depends(get_db)
):
    """ساخت توکن برای هاست زبیکس"""

    return repository_token.create_token(request, db)
