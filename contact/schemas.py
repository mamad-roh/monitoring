from fastapi import Query
from pydantic import BaseModel, EmailStr


class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def validate(cls, value: str) -> str:
        if value == "":
            return value
        return super().validate(value)


class InContactSchemas(BaseModel):
    class Config:
        orm_mode = True
    full_name: str = Query(None, min_length=4, max_length=50)
    # phone: Annotated[str, Field(max_length=14)]
    phone: str = Query(None, max_length=14)
    email: EmailEmptyAllowedStr = Query(None)
    telegram_id: str = Query(None, max_length=50)
    is_active: bool
    description: str = Query(None, max_length=255)


class OutContactSchemas(InContactSchemas):
    id: int


class InMigrationSchemas(BaseModel):
    class Config:
        orm_mode = True
    name: str
    type: str
    unique: bool
    nullable: bool
