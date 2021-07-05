from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from web_hook import schemas
from manage_server import models as m_s_models
from server import models as s_models
from media_manage import models as m_m_models
from media import models as m_models
from contact import models as c_models


def get_media_manage(
    _id: int,
    ip: str,
    db: Session
):
    """
    اگر آیدی منجرسرور در تیبل مدیا منجر وجود داشت
    عملیات ارسال را انجام دهد
    """

    data_media_manage = db.query(m_m_models.MediaManageModel).filter(
        m_m_models.MediaManageModel.manage_server_id == _id
    ).all()
    print(data_media_manage)

    # if not data_media_manage:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f'The MediaManage is not configured for the ServerManage with IP: {ip}'
    #     )

    for _object in data_media_manage:
        yield _object.media_id, _object.detail


def receive_post(
    request: schemas.InWebHookSchemas,
    db: Session
):
    """دریافت رکوئست هشدار از طرف زبیکس و ارسال آن به مخاطب"""

    # گرفتن آیدی سرور در صورت وجود آی پی
    server_id = db.query(s_models.ServerModel).filter(
        s_models.ServerModel.ip == request.ip,
        s_models.ServerModel.is_active == True
    ).first()
    if not server_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'ip {request.ip} not found or server is deactivate!'
        )

    # گرفتن تمام آبجکت های منجر سرور مربوط به آیدی سرور
    manage_server_object = db.query(m_s_models.ManageServer).filter(
        m_s_models.ManageServer.server_id == server_id.id
    ).all()
    del server_id
    if not manage_server_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'The ServerManage is not configured for the Server with IP: {request.ip}'
        )

    flag_1 = dict()
    for _object in manage_server_object:
        _id = _object.id

        c_id = _object.contact_id
        c_data = db.query(c_models.ContactModel).filter(
            c_models.ContactModel.id == c_id
        ).first()
        flag_2 = []
        for m_id, detail in get_media_manage(
            _id,
            request.ip,
            db
        ):

            flag_3 = []
            media_name = db.query(m_models.MediaModel).filter(
                m_models.MediaModel.id == m_id
            ).first().name

            if media_name == 'sms':
                if c_data.phone:
                    flag_3.append('sms send.')
            elif media_name == 'call':
                if c_data.phone:
                    flag_3.append('call send.')
            elif media_name == 'email':
                if c_data.email:
                    flag_3.append('email send.')
            elif media_name == 'tel':
                if c_data.telegram_id:
                    flag_3.append('telegram send.')
            else:
                # اگر مقدار آن ست نشده باشد برای جلوگیری از کرش
                continue
            flag_2.append(flag_3)
        flag_1[c_data.full_name] = flag_2
    print(flag_1)
    return flag_1
