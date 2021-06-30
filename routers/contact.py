from fastapi import Depends, status
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
def post_users(
    request: schemas.InContactSchemas,
    db: Session = Depends(get_db)
):
    """ساخت کانتکت جدید"""

    return repository.create(request, db)
