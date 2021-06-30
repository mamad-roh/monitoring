from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.sql.functions import mode
from contact import models


def check_contact(request: dict, db: Session):
    """چک کردن دیتا در صورت وجود نداشتن برای ساخت کانتکت جدید"""

    flag = dict()
    data = db.query(models.ContactModel)

    if data.filter(
        models.ContactModel.email == request.email
    ).first():
        flag['email'] = 'email is exist!'

    if data.filter(
        models.ContactModel.phone == request.phone
    ).first():
        flag['phone'] = 'phone is exist!'

    if data.filter(
        models.ContactModel.telegram_id == request.telegram_id
    ).first():
        flag['telegram'] = 'telegram is exist!'

    return flag


def create(request, db):
    """ساخت کانتکت جدید"""

    flag = check_contact(request, db)
    if flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=flag
        )
    else:
        new_contact = models.ContactModel(**request.dict())
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return {"detail": "account is created"}