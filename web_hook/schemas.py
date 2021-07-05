from pydantic import BaseModel


class InWebHookSchemas(BaseModel):
    class Config:
        orm_mode = True

    ip: str
    message: str
