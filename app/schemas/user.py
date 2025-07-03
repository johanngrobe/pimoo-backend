from typing import Optional

from fastapi_users import schemas
from pydantic import Field, ConfigDict
from uuid import UUID

from app.utils.enum_util import RoleEnum


class UserRead(schemas.BaseUser[UUID]):
    """
    Schema for reading user information, including associated municipality details.
    """

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    vorname: str = Field(..., description="User's first name.")
    nachname: str = Field(..., description="User's last name.")
    rolle: RoleEnum = Field(..., description="Role of the user in the system.")
    gemeinde_id: int = Field(..., description="ID of the associated municipality.")
    gemeinde: "GemeindeRead" = Field(
        ..., description="Detailed information about the associated municipality."
    )


class UserCreate(schemas.BaseUserCreate):
    """
    Schema for creating a new user, requiring essential details.
    """

    vorname: str = Field(..., description="User's first name.")
    nachname: str = Field(..., description="User's last name.")
    rolle: RoleEnum = Field(..., description="Role of the user in the system.")
    gemeinde_id: int = Field(..., description="ID of the associated municipality.")


class UserUpdate(schemas.BaseUserUpdate):
    """
    Schema for updating an existing user. All fields are optional for partial updates.
    """

    vorname: Optional[str] = Field(None, description="Updated first name of the user.")
    nachname: Optional[str] = Field(None, description="Updated last name of the user.")
    rolle: Optional[RoleEnum] = Field(
        None, description="Updated role of the user in the system."
    )
    gemeinde_id: Optional[int] = Field(
        None, description="Updated ID of the associated municipality."
    )


# Late import for forward references
from app.schemas.gemeinde import GemeindeRead
