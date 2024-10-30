from pydantic import BaseModel, ConfigDict ,EmailStr
from fastapi_users import schemas
from typing import Optional
from enum import Enum
from datetime import datetime
from uuid import UUID
from .municipality import MunicipalityOut

class RoleEnum(str, Enum):
    ADMINISTRATION = "administration"
    POLITICIAN = "politician"

class UserRead(schemas.BaseUser[UUID]):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    first_name: str
    last_name: str
    role: RoleEnum
    municipality_id: int
    municipality: MunicipalityOut


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    role: RoleEnum
    municipality_id: int


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    municipality_id: Optional[int] = None


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     id: Optional[UUID] = None
#     role: Optional[str] = None
#     municipality_id: Optional[int] = None