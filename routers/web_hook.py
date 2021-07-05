from fastapi import status, APIRouter, Depends
from web_hook import schemas, repository_v2
from database import database

router = APIRouter(
    tags=['WebHook'],
    prefix='/web_hook'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_200_OK)
def send_notif(
    request: schemas.InWebHookSchemas,
    db=Depends(get_db)
):

    return repository_v2.receive_post(request, db)
