from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing_extensions import Annotated


class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def validate(cls, value: str) -> str:
        if value == "":
            return value
        return super().validate(value)


class InContactSchemas(BaseModel):
    class Config:
        orm_mode = True
    full_name: Annotated[str, Field(min_length=4, max_length=50)]
    phone: Annotated[Optional[str], Field(max_length=14)]
    email: Optional[EmailEmptyAllowedStr]
    telegram_id: Annotated[Optional[str], Field(max_length=50)]
    is_active: Optional[bool]
    description: Annotated[Optional[str], Field(max_length=255)]


class OutContactSchemas(InContactSchemas):
    id: int
