from pydantic import BaseModel, Field, ConfigDict


class UserRolleBase(BaseModel):
    name: str = Field(..., description="Titel der Benutzerrolle")


class UserRolleCreate(UserRolleBase):
    pass


class UserRolleUpdate(UserRolleBase):
    pass


class UserRolleRead(UserRolleBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int = Field(..., description="ID der Benutzerrolle")
