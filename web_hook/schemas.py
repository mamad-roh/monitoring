from pydantic import BaseModel, IPvAnyAddress


class InTokenSchemas(BaseModel):
    class Config:
        orm_mode = True
    host_ip: IPvAnyAddress


class InWebHookSchemas(BaseModel):
    class Config:
        orm_mode = True

    ip: str
    message: str
    token: str


class GetTokenSchemas(BaseModel):
    class Config:
        orm_mode = True
    id: int
    host_ip: str
