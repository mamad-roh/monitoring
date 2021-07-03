from typing import List
from pydantic import BaseModel
from fastapi import Query


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


class INContactServerDelete(BaseModel):
    class Config:
        orm_mode = True
    server_id: int
    contact_id: int
