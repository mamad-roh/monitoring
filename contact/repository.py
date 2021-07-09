from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from contact import models, schemas


def set_null(request):
    """convert '' request to null"""
    if request.email is not None:
        if len(request.email) == 0:
            request.email = None
    if request.telegram_id is not None:
        if len(request.telegram_id) == 0:
            request.telegram_id = None
    if request.phone is not None:
        if len(request.phone) == 0:
            request.phone = None
    return request


def check_contact(request: dict, db: Session):
    """چک کردن دیتا در صورت وجود نداشتن برای ساخت کانتکت جدید"""

    flag = dict()
    data = db.query(models.ContactModel)

    if data.filter(
        models.ContactModel.full_name == request.full_name
    ).first():
        if request.full_name:
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


def check_update_exist(_object, method, _id, db):
    """check item exist request for update"""

    if db.filter(_object == method).filter(
        models.ContactModel.id != _id
    ).first() and method:
        return False
    return True


def create(request, db):
    """ساخت مخاطب جدید"""

    flag = check_contact(request, db)
    if flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=flag
        )
    else:
        request = set_null(request)
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

    query_db = db.query(models.ContactModel)
    contact = query_db.filter(
        models.ContactModel.id == _id
    )
    if not contact.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    request = set_null(request)
    flag = dict()
    if not check_update_exist(
        models.ContactModel.full_name,
        request.full_name,
        _id,
        query_db
    ):
        flag['name'] = 'name is exist!'

    if not check_update_exist(
        models.ContactModel.email,
        request.email,
        _id,
        query_db
    ):
        flag['email'] = 'email is exist!'

    if not check_update_exist(
        models.ContactModel.phone,
        request.phone,
        _id,
        query_db
    ):
        flag['phone'] = 'phone is exist!'

    if not check_update_exist(
        models.ContactModel.telegram_id,
        request.telegram_id,
        _id,
        query_db
    ):
        flag['telegram'] = 'telegram is exist!'

    if not flag:
        contact.update(request.dict())
        db.commit()
        return {'detail': f'Contact with the ID: {_id} is updated.'}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=flag
        )

#    test = select(models.ContactModel).where(models.ContactModel.id != _id)
#     result = db.execute(test)
#     print(result, result.scalars())
#     for item in result.scalars():
#         print(item)
#         print(item.id)
#         print('*' * 10)


def delete(db, _id: int):
    """پاک کردن یک مخاطب در صورت وجود"""

    contact = db.query(models.ContactModel).filter(
        models.ContactModel.id == _id
    ).first()

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with the ID: {_id} not available"
        )
    db.delete(contact)
    db.commit()
    return {'detail': f'Contact with the ID: {_id} is deleted.'}


def set_migration(
    request: schemas.InMigrationSchemas,
    db: Session
):
    # ### alembic fastapi >>
    # 'https://harrisonmorgan.dev/2021/02/15/getting-started-with-fastapi-users-and-alembic/'
    # if request.type == 'str':
    #     col = Column(
    #         request.name,
    #         String,
    #         unique=request.unique)
    #     col.create(models.ContactModel, populate_default=True)
    pass
