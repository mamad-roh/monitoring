from typing import List
from pydantic import BaseModel
from fastapi import Query
from server import schemas as s_schemas
from contact import schemas as c_schemas


class InServerInContacts(BaseModel):
    class Config:
        orm_mode = True

    server_id: int
    contact_id: List[int] = Query(None, min_items=1)


class InContactInServers(BaseModel):
    class Config:
        orm_mode = True

    server_id: List[int] = Query(None, min_items=1)
    contact_id: int


class OutContactServerGet(BaseModel):
    class Config:
        orm_mode = True
    id: int
    server_id: int
    contact_id: int
    parant_server: s_schemas.OutServerGet
    parant_contact: c_schemas.OutContactSchemas


class INContactServerDelete(BaseModel):
    class Config:
        orm_mode = True
    server_id: int
    contact_id: int
