from sqlalchemy.orm import Session
from manage_server import schemas, models
from contact import models as c_models
from server import models as s_models
from fastapi import HTTPException, status


def set_object(_id: int, ls: list, act: str):
    list_object = []

    if act == 'server':
        for item in ls:

            params = {
                'server_id': _id,
                'contact_id': item
            }
            list_object.append(models.ManageServer(**params))
        return list_object


def check_contact(db: Session, ls: list):
    flag = dict()
    for _id in ls:
        if not db.query(
            c_models.ContactModel
        ).filter(c_models.ContactModel.id == _id).first():
            flag[f'{_id}'] = f"Contact with the ID: {_id} not available"
    return flag


def check_server(db, ls: tuple):
    flag = dict()
    for _id in ls:
        if not db.query(
            s_models.ServerModel
        ).filter(s_models.ServerModel.id == _id).first():
            flag[f'{_id}'] = f"Server with the ID: {_id} not available"
    return flag


def create_server_contacts(request: schemas.InServerInContacts, db: Session):
    request.contact_id = set(request.contact_id)
    request.server_id = (request.server_id, )
    c_flag = check_contact(db, request.contact_id)
    s_flag = check_server(db, request.server_id)
    if c_flag or s_flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'server': s_flag,
                'contact': c_flag
            }
        )

    list_object = set_object(request.server_id, request.contact_id, 'server')
    db.bulk_save_objects(list_object)
    db.commit()
    return {'detail': 'list is added.'}


def create_contact_servers(request: schemas.InContactInServers, db: Session):
    request.server_id = set(request.server_id)
    request.contact_id = (request.contact_id, )
    c_flag = check_contact(db, request.contact_id)
    s_flag = check_server(db, request.server_id)
    if c_flag or s_flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'server': s_flag,
                'contact': c_flag
            }
        )

    list_object = set_object(request.contact_id, request.server_id, 'contact')
    db.bulk_save_objects(list_object)
    db.commit()
    return {'detail': 'list is added.'}
