from fastapi import status
from fastapi import APIRouter

router = APIRouter(
    tags=['WebHook'],
    prefix='/web_hook'
)


@router.post('/', status_code=status.HTTP_200_OK)
def send_notif(request: dict):
    print(request)
    return request
