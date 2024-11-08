from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class MainObjectiveBase(BaseModel):
    """
    Base schema for a main objective, containing the primary number and label.
    """

    no: int = Field(
        ..., description="The unique number representing the main objective."
    )
    label: str = Field(..., description="A descriptive label for the main objective.")


class MainObjectiveCreate(MainObjectiveBase):
    """
    Schema for creating a new main objective.
    """

    pass


class MainObjectiveUpdate(BaseModel):
    """
    Schema for updating an existing main objective, allowing partial updates.
    """

    no: Optional[int] = Field(
        None, description="The updated number for the main objective."
    )
    label: Optional[str] = Field(
        None, description="The updated label for the main objective."
    )


class MainObjectiveBasicRead(MainObjectiveBase):
    """
    Basic read schema for a main objective, includes the ID.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the main objective.")


class MainObjectiveFullRead(MainObjectiveBase):
    """
    Detailed read schema for a main objective, including metadata and sub-objectives.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the main objective.")
    municipality_id: int = Field(..., description="ID of the associated municipality.")
    sub_objectives: List["SubObjectiveBasicRead"] = Field(
        default_factory=list, description="List of associated sub-objectives."
    )
    municipality: "MunicipalityRead" = Field(
        ..., description="The municipality associated with this main objective."
    )
    author: Optional["UserRead"] = Field(
        None, description="User who created the main objective."
    )
    last_editor: Optional["UserRead"] = Field(
        None, description="User who last edited the main objective."
    )


# Late imports for forward references
from app.schemas.municipality_schema import MunicipalityRead
from app.schemas.sub_objective_schema import SubObjectiveBasicRead
from app.schemas.user_schema import UserRead
