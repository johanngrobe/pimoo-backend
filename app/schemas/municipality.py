from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MunicipalityBase(BaseModel):
    """
    Base schema for a municipality, containing the primary name attribute.
    """

    name: str = Field(..., description="The name of the municipality.")


class MunicipalityCreate(MunicipalityBase):
    """
    Schema for creating a new municipality. Inherits fields from MunicipalityBase.
    """

    pass


class MunicipalityUpdate(BaseModel):
    """
    Schema for updating an existing municipality. Allows partial updates.
    """

    name: Optional[str] = Field(
        None, description="The updated name of the municipality."
    )


class MunicipalityRead(MunicipalityBase):
    """
    Read schema for a municipality, including the unique identifier.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the municipality.")
