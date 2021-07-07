from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from typing_extensions import Annotated


class EmailEmptyAllowedStr(EmailStr):
    @classmethod
    def validate(cls, value: str) -> str:
        if value == "":
            return value
        return super().validate(value)


class UserSchemas(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: Optional[bool]
    is_staff: Optional[bool]
    password: str


class UserPostSchemas(BaseModel):
    class Config:
        orm_mode = True
    username: Annotated[str, Field(min_length=4, max_length=12)]
    is_active: Optional[bool]
    is_staff: Optional[bool]
    password: Annotated[str, Field(min_length=6, max_length=16)]


class OutUserSchemas(BaseModel):
    class Config:
        orm_mode = True
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_staff: Optional[bool]


class OutUserPutSchemas(BaseModel):
    class Config:
        orm_mode = True
    username: str
    first_name: str
    last_name: str
    email: EmailEmptyAllowedStr
    is_active: Optional[bool]
    is_staff: Optional[bool]


class InLoginSchemas(BaseModel):
    class Config:
        orm_mode: True
    username: str
    password: str
