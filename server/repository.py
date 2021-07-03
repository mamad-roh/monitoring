from sqlalchemy.orm import Session
from server import schemas, models
from fastapi import HTTPException, status


def set_null(request):
    """convert '' request to null"""

    if len(request.name) == 0:
        request.name = None
    if len(request.ip) == 0:
        request.ip = None

    return request


def check_update_exist(_object, method, _id, db):
    """check item exist request for update"""

    if db.filter(_object == method).filter(
        models.ServerModel.id != _id
    ).first():
        return False
    return True


def check_server(request: schemas.InServerSchemas, db: Session):
    """چک کردن دیتا در صورت وجود نداشتن برای ساخت سرور جدید"""

    flag = dict()
    data = db.query(models.ServerModel)
    if data.filter(
        models.ServerModel.name == request.name
    ).first():
        if request.name:
            flag['name'] = 'server name is exist!'

    if data.filter(
        models.ServerModel.ip == request.ip.__str__()
    ).first():
        if request.ip:
            flag['ip'] = 'ip address is exist!'

    return flag


def create_server(request: schemas.InServerSchemas, db: Session):
    flag = check_server(request, db)
    if flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=flag
        )

    request.ip = request.ip.__str__()
    request = set_null(request)
    new_contact = models.ServerModel(**request.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"detail": "server is added."}


def get_servers(db: Session):
    servers = db.query(models.ServerModel).all()
    if not servers:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Server list is empty."
        )
    return servers


def get_server(_id, db: Session):
    server = db.query(models.ServerModel).filter(
        models.ServerModel.id == _id
    ).first()

    if not server:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Server with the ID: {_id} not available"
        )
    return server


def update_server(
    _id: int,
    request: schemas.InServerSchemas,
    db: Session
):
    query_db = db.query(models.ServerModel)
    server = query_db.filter(
        models.ServerModel.id == _id
    )
    if not server.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with the ID: {_id} not available"
        )

    request.ip = request.ip.__str__()
    request = set_null(request)

    flag = dict()
    if not check_update_exist(
        models.ServerModel.name,
        request.name,
        _id,
        query_db
    ):
        flag['name'] = 'name is exist!'

    if not check_update_exist(
        models.ServerModel.ip,
        request.ip,
        _id,
        query_db
    ):
        flag['ip'] = 'ip is exist!'

    if not flag:
        server.update(request.dict())
        db.commit()
        return {'detail': f'Server with the ID: {_id} is updated.'}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=flag
        )


def delete_server(_id: int, db: Session):

    server = db.query(models.ServerModel).filter(
        models.ServerModel.id == _id
    ).first()

    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Server with the ID: {_id} not available"
        )
    db.delete(server)
    db.commit()
    return {'detail': f'Server with the ID: {_id} is deleted.'}
