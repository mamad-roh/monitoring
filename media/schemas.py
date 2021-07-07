# from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class InMediaSchemas(BaseModel):
    class Config:
        orm_mode = True
    name: str = Query(None, min_length=3, max_length=12)
    is_active: bool


class OutMediaSchemasGet(InMediaSchemas):
    id: int


class InMediaSchemasUpdate(BaseModel):
    class Config:
        orm_mode = True
    is_active: bool
