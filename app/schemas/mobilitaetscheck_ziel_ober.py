from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class MobilitaetscheckZielOberBase(BaseModel):
    """
    Base schema for a main objective, containing the primary number and label.
    """

    nr: int = Field(
        ..., description="The unique number representing the main objective."
    )
    name: str = Field(..., description="A descriptive label for the main objective.")


class MobilitaetscheckZielOberCreate(MobilitaetscheckZielOberBase):
    """
    Schema for creating a new main objective.
    """

    pass


class MobilitaetscheckZielOberUpdate(BaseModel):
    """
    Schema for updating an existing main objective, allowing partial updates.
    """

    nr: Optional[int] = Field(
        None, description="The updated number for the main objective."
    )
    name: Optional[str] = Field(
        None, description="The updated label for the main objective."
    )


class MobilitaetscheckZielOberBaseRead(MobilitaetscheckZielOberBase):
    """
    Basic read schema for a main objective, includes the ID.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the main objective.")


class MobilitaetscheckZielOberRead(MobilitaetscheckZielOberBase):
    """
    Detailed read schema for a main objective, including metadata and sub-objectives.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the main objective.")
    gemeinde_id: int = Field(..., description="ID of the associated municipality.")
    ziel_unter: List["MobilitaetscheckZielUnterBaseRead"] = Field(
        default_factory=list, description="List of associated sub-objectives."
    )
    gemeinde: "GemeindeRead" = Field(
        ..., description="The municipality associated with this main objective."
    )
    autor: Optional["UserRead"] = Field(
        None, description="User who created the main objective."
    )
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the main objective."
    )


# Late imports for forward references
from app.schemas.gemeinde import GemeindeRead
from app.schemas.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnterBaseRead
from app.schemas.user import UserRead
