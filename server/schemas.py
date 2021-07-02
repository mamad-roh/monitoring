from typing import Optional
from pydantic import BaseModel, IPvAnyAddress
from fastapi import Query


class InServerSchemas(BaseModel):
    class Config:
        orm_mode = True
    name: str = Query(None, min_length=1, max_length=50)
    ip: IPvAnyAddress
    is_active: Optional[bool]
    description: Optional[str] = Query(None, max_length=255)
