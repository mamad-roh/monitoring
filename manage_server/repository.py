from sqlalchemy.orm import Session
from manage_server import schemas, models
from contact import models as c_models
from server import models as s_models
from fastapi import HTTPException, status


def set_object(_id: int, ls: set, act: str):
    """گرفتن لیست از ایدی ها و تبدیل ان به آبجکت برای ذخیره در دیتابیس"""

    list_object = []
    if act == 'server':
        for item in ls:
            params = {
                'server_id': _id,
                'contact_id': item
            }
            list_object.append(models.ManageServer(**params))
    elif act == 'contact':
        for item in ls:
            params = {
                'contact_id': _id,
                'server_id': item
            }
            list_object.append(models.ManageServer(**params))
    return list_object


def check_contact(db: Session, ls: set):
    """
    گرفتن لیستی از آیدی مخاطب
    چک کند که این مخاطب وجود دارد یا خیر
    """

    flag = dict()
    for _id in ls:
        if not db.query(
            c_models.ContactModel
        ).filter(c_models.ContactModel.id == _id).first():
            flag[f'{_id}'] = f"Contact with the ID: {_id} not available"
    return flag


def check_server(db, ls: set):
    """
    گرفتن لیستی از آیدی سرور
    چک کند که این سرور وجود دارد یا خیر
    """

    flag = dict()
    for _id in ls:
        if not db.query(
            s_models.ServerModel
        ).filter(s_models.ServerModel.id == _id).first():
            flag[f'{_id}'] = f"Server with the ID: {_id} not available"
    return flag


def check_list(db, _id: int, ls: set, act: str):
    """
    اگر ایدی از ایتمی از قبل در دیتا بیس ذخیره شده باشد
    آن را از لیست رکوئست ها پاک میکنیم
    """

    new_ls = set(ls)
    data = db.query(models.ManageServer)
    if act == 'server':
        for contact_id in ls:
            if data.filter(
                models.ManageServer.server_id == _id,
                models.ManageServer.contact_id == contact_id
            ).first():
                new_ls.remove(contact_id)
    elif act == 'contact':
        for server_id in ls:
            if data.filter(
                models.ManageServer.contact_id == _id,
                models.ManageServer.server_id == server_id
            ).first():
                new_ls.remove(server_id)

    if new_ls:
        return new_ls

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail={'detail': 'added.'}
    )


def create_server_contacts(request: schemas.InServerInContacts, db: Session):
    request.contact_id = set(request.contact_id)
    request.contact_id = check_list(
        db,
        request.server_id,
        request.contact_id,
        'server'
    )
    c_flag = check_contact(db, request.contact_id)
    s_flag = check_server(db, (request.server_id, ))
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
    request.server_id = check_list(
        db,
        request.contact_id,
        request.server_id,
        'contact'
    )
    c_flag = check_contact(db, (request.contact_id, ))
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


def delete_manage_server(
    request: schemas.INContactServerDelete,
    db: Session
):

    c_id = request.contact_id
    s_id = request.server_id
    data = db.query(models.ManageServer)
    contact = data.filter(
        models.ManageServer.contact_id == c_id
    )
    if contact.first():

        server = contact.filter(
            models.ManageServer.server_id == s_id
        )
        if server.first():
            db.delete(server.first())
            db.commit()
            return {'detail': f'Server with the ID: {s_id} is deleted.'}
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'detail': f'Server with the ID: {s_id} not available.'
            }
        )
    raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'detail': f'Contact with the ID: {c_id} not available.'
            }
        )


def get_all_manage_server(db: Session):

    data = db.query(models.ManageServer).all()
    if data:
        return data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={'detail': 'ManageServer list is empty.'}
    )


def get_manage_server(name: str, _id: int, db: Session):
    if name == 'server':
        data = db.query(models.ManageServer).filter(
            models.ManageServer.server_id == _id
        ).all()
        if data:
            return data
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Server with ID: {_id} not found.'}
        )
    elif name == 'contact':
        data = db.query(models.ManageServer).filter(
            models.ManageServer.contact_id == _id
        ).all()
        if data:
            return data
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'detail': f'Contact with ID: {_id} not found.'}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
