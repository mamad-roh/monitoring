from sqlalchemy.orm import Session
from media import schemas, models
from fastapi import HTTPException, status


def create_media(
    request: schemas.InMediaSchemas,
    db: Session
):
    """اضافه کردن مدیا جدید در صورتی که نام آن از قبل وجود نداشته باشد"""

    if db.query(models.MediaModel).filter(
        models.MediaModel.name == request.name
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Media name: {request.name} is exist.'
        )
    flag = ['sms', 'call', 'tel', 'email']
    if request.name in flag:
        new_media = models.MediaModel(**request.dict())
        db.add(new_media)
        db.commit()
        return {"detail": "Media is added."}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Media name must be: {flag}'
        )
        # return {'detail': f'Media name must be: {flag}'}


def get_all_media(db: Session):
    """برگشت تمام مدیا در صورت وجود"""

    media = db.query(models.MediaModel).all()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Media list is empty.'
        )

    return media


def get_media(_id: int, db: Session):
    """برگشت یک مدیا در صورت وجود"""

    media = db.query(models.MediaModel).filter(
        models.MediaModel.id == _id
    ).first()

    if not media:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Media with the ID: {_id} not available.'
        )

    return media


def update_media(
    _id: int,
    request: schemas.InMediaSchemas,
    db: Session
):
    """آپدیت مدیا در صورت وجود"""

    db_query = db.query(models.MediaModel)
    media = db_query.filter(
        models.MediaModel.id == _id
    )
    if not media.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Media with the ID: {_id} not available.'
        )

    # if db_query.filter(
    #     models.MediaModel.name == request.name,
    #     models.MediaModel.id != _id
    # ).first():
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail='Media name is exist.'
    #     )

    media.update(request.dict())
    db.commit()
    return {'detail': f'Media with the ID: {_id} is updated.'}


def delete_media(_id: int, db: Session):
    """دلیت کردن مدیا در صورت وجود"""

    media = db.query(models.MediaModel).filter(
        models.MediaModel.id == _id
    ).first()

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media with the ID: {_id} not available"
        )
    db.delete(media)
    db.commit()
    return {'detail': f'Media with the ID: {_id} is deleted.'}
