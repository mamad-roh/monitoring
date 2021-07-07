from sqlalchemy.orm import Session
from passlib.context import CryptContext
from web_hook import schemas, models
from fastapi import HTTPException, status
import uuid

# ##### make hash password >>
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_token(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_token_hash(password):
    return pwd_context.hash(password)
# ## <<


def check_ip(request: schemas.InTokenSchemas, db: Session):

    data = db.query(models.TokenModel)
    if data.filter(
        models.TokenModel.host_ip == request.host_ip.__str__()
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'ip: {request.host_ip.__str__()} is exist in database!'
        )
    return True


def create_token(
    request: schemas.InTokenSchemas,
    db: Session
):

    if check_ip(request, db):
        _id = uuid.uuid1()
        token = get_token_hash(str(_id))
        new_request = dict(request)
        new_request['token'] = token
        new_request['host_ip'] = request.host_ip.__str__()
        new_token = models.TokenModel(**new_request)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return {
            "detail": f"token for {request.host_ip.__str__()} is created.",
            "token": token
        }


def update_token(
    request: schemas.InTokenUpdateSchemas,
    db: Session
):
    db_query = db.query(models.TokenModel)
    media = db_query.filter(
        models.TokenModel.H == _id
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



def delete_token(db: Session):
    pass
