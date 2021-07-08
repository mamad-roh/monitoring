from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from web_hook import schemas, models
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

    # if not data_media_manage:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f'The MediaManage is not configured for the ServerManage with IP: {ip}'
    #     )

    for _object in data_media_manage:
        yield _object.media_id, _object.detail


def send_massage_contact(
    c_data,
    m_id,
    db
):
    flag = []
    media = db.query(m_models.MediaModel).filter(
        m_models.MediaModel.id == m_id
    ).first()

    if media.name == 'sms':
        if media.is_active:
            if c_data.phone:
                flag.append('sms send.')
        else:
            flag.append('sms is deactivate!')
    elif media.name == 'call':
        if media.is_active:
            if c_data.phone:
                flag.append('call send.')
        else:
            flag.append('call is deactivate!')
    elif media.name == 'email':
        if media.is_active:
            if c_data.email:
                flag.append('email send.')
        else:
            flag.append('email is deactivate!')
    elif media.name == 'tel':
        if media.is_active:
            if c_data.telegram_id:
                flag.append('telegram send.')
        else:
            flag.append('telegram is deactivate!')
    else:
        # اگر مقدار آن ست نشده باشد برای جلوگیری از کرش
        return None

    return flag


def check_token(request, db: Session):
    is_token = db.query(models.TokenModel).filter(
        models.TokenModel.host_ip == request.ip
    ).first()
    if is_token:
        if request.token == is_token.token:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'token dose not set for HostIP: {request.ip}'
        )


def receive_post(
    request: schemas.InWebHookSchemas,
    db: Session,
):
    """دریافت رکوئست هشدار از طرف زبیکس و ارسال آن به مخاطب"""

    check_token(request, db)

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
            if c_data.is_active:
                flag_2.append(send_massage_contact(
                    c_data,
                    m_id,
                    db
                ))
            else:
                flag_2.append(f'Contact: {c_data.full_name} is deactivate')
        c_n = c_data.full_name
        if not flag_2:
            flag_1[c_n] = f'The MediaManage is not configured for the Contact with: {c_n}'
        else:
            flag_1[c_n] = flag_2
    print(flag_1)
    return {'detail': flag_1}
