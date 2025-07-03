from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MobilitaetscheckZielUnterBase(BaseModel):
    """
    Base schema for a sub-objective, containing the primary fields.
    """

    nr: int = Field(
        ..., description="The unique number representing the sub-objective."
    )
    name: str = Field(..., description="A descriptive label for the sub-objective.")
    ziel_ober_id: int = Field(
        ..., description="ID of the main objective associated with this sub-objective."
    )


class MobilitaetscheckZielUnterCreate(MobilitaetscheckZielUnterBase):
    """
    Schema for creating a new sub-objective. Inherits fields from MobilitaetscheckZielUnterBase.
    """

    pass


class MobilitaetscheckZielUnterUpdate(BaseModel):
    """
    Schema for updating an existing sub-objective. All fields are optional to allow partial updates.
    """

    nr: Optional[int] = Field(None, description="Updated number for the sub-objective.")
    name: Optional[str] = Field(
        None, description="Updated label for the sub-objective."
    )
    ziel_ober_id: Optional[int] = Field(
        None, description="Updated ID of the associated main objective."
    )


class MobilitaetscheckZielUnterBaseRead(MobilitaetscheckZielUnterBase):
    """
    Basic read schema for a sub-objective, including the unique identifier and municipality ID.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the sub-objective.")
    gemeinde_id: int = Field(
        ..., description="ID of the municipality associated with this sub-objective."
    )


class MobilitaetscheckZielUnterRead(MobilitaetscheckZielUnterBase):
    """
    Detailed read schema for a sub-objective, including related main objective, municipality, and author information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the sub-objective.")
    ziel_ober: "MobilitaetscheckZielOberBaseRead" = Field(
        ..., description="Basic details of the associated main objective."
    )
    gemeinde_id: int = Field(
        ..., description="ID of the municipality associated with this sub-objective."
    )
    gemeinde: "GemeindeRead" = Field(
        ..., description="Detailed information about the associated municipality."
    )
    autor: Optional["UserRead"] = Field(
        None, description="User who created the sub-objective."
    )
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the sub-objective."
    )


# Late imports for forward references
from app.schemas.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOberBaseRead
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user import UserRead
