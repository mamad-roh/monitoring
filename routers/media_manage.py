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


@router.get(
    '/{_id}',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.OutMediaManageSchemas]
)
def get_media_manager(_id, db=Depends(get_db)):

    return repository.gat_media_manage(_id, db)


@router.delete('/', status_code=status.HTTP_200_OK)
def delete_media_manage(
    request: schemas.InMediaManageSchemasDelete,
    db=Depends(get_db)
):

    return repository.delete_media_manage(request, db)
