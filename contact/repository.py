from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.sql.functions import mode
from starlette import responses
from contact import models


def check_contact(request: dict, db: Session):
    """چک کردن دیتا در صورت وجود نداشتن برای ساخت کانتکت جدید"""

    flag = dict()
    data = db.query(models.ContactModel)

    if data.filter(
        models.ContactModel.full_name == request.full_name
    ).first():
        if request.email:
            flag['name'] = 'full name is exist!'

    if data.filter(
        models.ContactModel.email == request.email
    ).first():
        if request.email:
            flag['email'] = 'email is exist!'

    if data.filter(
        models.ContactModel.phone == request.phone
    ).first():
        if request.phone:
            flag['phone'] = 'phone is exist!'

    if data.filter(
        models.ContactModel.telegram_id == request.telegram_id
    ).first():
        if request.telegram_id:
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


def get_contact(db, _id: int):
    """برگشت یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).first()
    if not contact:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Contact with the ID: {_id} not available"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    return contact


def get_contacts(db):
    """برگشت تمام مخاطبین در صورت وجود"""

    contacts = db.query(models.ContactModel).all()

    if not contacts:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Contact list is empty'
        )
    return contacts


def update_contact(_id: int, request, db: Session):
    """آپدیت مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    

    db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).update(request.dict())
    db.commit()
    return {'detail': f'Contact with the ID: {_id} is updated.'}
