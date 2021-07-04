from typing import List
from fastapi.param_functions import Query
from pydantic import BaseModel
from manage_server import schemas as m_s_schemas
from media import schemas as m_schemas


class InMediaManageSchemas(BaseModel):
    class Config:
        orm_mode = True

    manage_server_id: int
    media: List[dict] = Query(
        [{
            'media_id': 0,
            'detail': 'str'
        }],
        min_items=1
    )


class InMediaManageSchemasDelete(BaseModel):
    class Config:
        orm_mode = True

    manage_server_id: int
    media_id: int


class InMediaManageSchemasUpdate(InMediaManageSchemasDelete):
    description: str


class OutMediaManageSchemas(BaseModel):
    class Config:
        orm_mode = True

    id: int
    manage_server_id: int
    media_id: int
    parant_media: m_schemas.OutMediaSchemasGet
    parant_manage_server: m_s_schemas.INContactServerDelete
