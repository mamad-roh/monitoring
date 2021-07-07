from media_manage import schemas
from sqlalchemy.orm import Session
from media_manage import models
from media import models as m_models
from manage_server import models as m_s_models
from fastapi import HTTPException, status


def set_object(_id: int, ls: set):
    """گرفتن لیست از ایدی ها و تبدیل ان به آبجکت برای ذخیره در دیتابیس"""

    list_object = []

    for item in ls:
        params = {
            'manage_server_id': _id,
            **item
        }
        list_object.append(models.MediaManageModel(**params))

    return list_object


def check_media(db: Session, ls: set):
    """
    گرفتن لیستی از آیدی مدیا
    چک کند که این مدیا وجود دارد یا خیر
    """

    flag = dict()
    for item in ls:
        _id = item['media_id']
        if not db.query(
            m_models.MediaModel
        ).filter(m_models.MediaModel.id == _id).first():
            flag[f'{_id}'] = f"Media with the ID: {_id} not available"
    return flag


def check_manage_server(db, ls: set):
    """
    گرفتن لیستی از آیدی سرور منیجر
    چک کند که این سرور منیجر وجود دارد یا خیر
    """

    flag = dict()
    for _id in ls:
        if not db.query(
            m_s_models.ManageServer
        ).filter(m_s_models.ManageServer.id == _id).first():
            flag[f'{_id}'] = f"ManageServer with the ID: {_id} not available"
    return flag


def check_list(db, _id: int, ls: set):
    """
    اگر ایدی از ایتمی از قبل در دیتا بیس ذخیره شده باشد
    آن را از لیست رکوئست ها پاک میکنیم
    """

    data = db.query(models.MediaManageModel)
    flag = []
    new_ls = list(ls)

    for item in ls:
        if data.filter(
            models.MediaManageModel.manage_server_id == _id,
            models.MediaManageModel.media_id == item['media_id']
        ).first():
            new_ls.remove(item)
        elif item['media_id'] in flag:
            new_ls.remove(item)
        else:
            flag.append(item['media_id'])

    if new_ls:
        return new_ls

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail='added.'
    )


def create_media_manage(
    request: schemas.InMediaManageSchemas,
    db: Session
):
    manage_server_id = request.manage_server_id
    media = request.media
    media = check_list(
        db,
        manage_server_id,
        media
    )
    m_s_flag = check_manage_server(
        db,
        (manage_server_id, )
    )
    media_flag = check_media(
        db,
        media
    )
    if m_s_flag or media_flag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'manage_server': m_s_flag,
                'media': media_flag
            }
        )

    list_object = set_object(manage_server_id, media)
    db.bulk_save_objects(list_object)
    db.commit()
    return {'detail': 'list is added.'}


def get_all_media_manage(db: Session):

    data = db.query(models.MediaManageModel).all()
    if data:
        return data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='MediaManageModel list is empty.'
    )


def gat_media_manage(_id: int, db: Session):

    data = db.query(models.MediaManageModel).filter(
        models.MediaManageModel.manage_server_id == _id
    ).all()
    if data:
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'ManageServer with ID: {_id} not found.'
    )


def delete_media_manage(
    request: schemas.InMediaManageSchemasDelete,
    db: Session
):
    m_id = request.media_id
    m_s_id = request.manage_server_id
    data = db.query(models.MediaManageModel)
    data = data.filter(
        models.MediaManageModel.media_id == m_id,
        models.MediaManageModel.manage_server_id == m_s_id,
    ).first()
    if data:
        db.delete(data)
        db.commit()
        return {'detail': f'table ID: {m_s_id}/{m_id} is deleted!'}

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'table ID: {m_s_id}/{m_id} not found!'
        )
