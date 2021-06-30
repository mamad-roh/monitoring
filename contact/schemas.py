from pydantic import BaseModel, EmailStr
from typing import Optional


class InContactSchemas(BaseModel):
    full_name: str
    phone: Optional[str]
    email: Optional[EmailStr]
    telegram_id: Optional[str]
    is_active: bool
    description: Optional[str]
