from fastapi import status, APIRouter, Depends, Request
from web_hook import schemas, repository_v2, repository_token
from database import database
from typing import List
from jwt_token import jwt

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
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):
    """ساخت توکن برای هاست زبیکس"""

    return repository_token.create_token(request, db)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.GetTokenSchemas]
)
def get_host_ip(
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository_token.get_host_ip(db)


@router.delete('/{_id}', status_code=status.HTTP_200_OK)
def delete_host_ip(
    _id: int,
    db=Depends(get_db),
    current_user=Depends(
        jwt.get_current_active_user
    )
):

    return repository_token.delete_token(_id, db)
