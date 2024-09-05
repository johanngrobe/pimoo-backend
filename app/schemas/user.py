from pydantic import BaseModel, ConfigDict ,EmailStr
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class UserBase(BaseModel):
    email: EmailStr

class UserCredentials(UserBase):
    first_name: str
    last_name: str
    organization: str
    street: str
    house_number: str
    postal_code: str
    city: str
    country: str

class UserCreate(UserCredentials):
    password: str

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None