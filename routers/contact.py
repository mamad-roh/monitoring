from fastapi import Depends, status
from starlette.status import HTTP_102_PROCESSING, HTTP_200_OK
from database import database
from sqlalchemy.orm import Session
from fastapi import APIRouter
from contact import schemas, repository


router = APIRouter(
    tags=['Contact'],
    prefix='/contact'
)

get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def post_contacts(
    request: schemas.InContactSchemas,
    db: Session = Depends(get_db)
):
    """ساخت مخاطب جدید"""

    return repository.create(request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_contacts(db: Session = Depends(get_db)):
    """برگشت تمام مخاطبین در صورت وجود"""

    return repository.get_contacts(db)


@router.get('/{_id}', status_code=status.HTTP_200_OK)
def get_contact(
    _id: int,
    db: Session = Depends(get_db)
):
    """برگشت یک مخاطب در صورت وجود"""

    return repository.get_contact(db, _id)


@router.put('/{_id}', status_code=status.HTTP_202_ACCEPTED)
def update_contact(
    _id: int,
    request: schemas.InContactSchemas,
    db: Session = Depends(get_db)
):
    """آپدیت کردن مخاطب در صورت وجود"""

    return repository.update_contact(_id, request, db)


# status_code=HTTP_204_NO_CONTENT
@router.delete('/{_id}', status_code=HTTP_200_OK)
def delete_contact(
        _id: int,
        db: Session = Depends(get_db),
):
    """پاک کردن یک مخاطب در صورت وجود"""

    return repository.delete(db, _id)
