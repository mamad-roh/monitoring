from database import database
from fastapi import APIRouter, status, Depends
from media_manage import schemas, repository
from typing import List

router = APIRouter(
    tags=['MediaManage'],
    prefix='/media_manage'
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_media_manage(
    request: schemas.InMediaManageSchemas,
    db=Depends(get_db)
):

    return repository.create_media_manage(request, db)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.OutMediaManageSchemas]
)
def get_all_media_manage(db=Depends(get_db)):

    return repository.get_all_media_manage(db)
