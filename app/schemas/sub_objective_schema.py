from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SubObjectiveBase(BaseModel):
    """
    Base schema for a sub-objective, containing the primary fields.
    """

    no: int = Field(
        ..., description="The unique number representing the sub-objective."
    )
    label: str = Field(..., description="A descriptive label for the sub-objective.")
    main_objective_id: int = Field(
        ..., description="ID of the main objective associated with this sub-objective."
    )


class SubObjectiveCreate(SubObjectiveBase):
    """
    Schema for creating a new sub-objective. Inherits fields from SubObjectiveBase.
    """

    pass


class SubObjectiveUpdate(BaseModel):
    """
    Schema for updating an existing sub-objective. All fields are optional to allow partial updates.
    """

    no: Optional[int] = Field(None, description="Updated number for the sub-objective.")
    label: Optional[str] = Field(
        None, description="Updated label for the sub-objective."
    )
    main_objective_id: Optional[int] = Field(
        None, description="Updated ID of the associated main objective."
    )


class SubObjectiveBasicRead(SubObjectiveBase):
    """
    Basic read schema for a sub-objective, including the unique identifier and municipality ID.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the sub-objective.")
    municipality_id: int = Field(
        ..., description="ID of the municipality associated with this sub-objective."
    )


class SubObjectiveFullRead(SubObjectiveBase):
    """
    Detailed read schema for a sub-objective, including related main objective, municipality, and author information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the sub-objective.")
    main_objective: "MainObjectiveBasicRead" = Field(
        ..., description="Basic details of the associated main objective."
    )
    municipality_id: int = Field(
        ..., description="ID of the municipality associated with this sub-objective."
    )
    municipality: "MunicipalityRead" = Field(
        ..., description="Detailed information about the associated municipality."
    )
    author: Optional["UserRead"] = Field(
        None, description="User who created the sub-objective."
    )
    last_editor: Optional["UserRead"] = Field(
        None, description="User who last edited the sub-objective."
    )


# Late imports for forward references
from app.schemas.main_objective_schema import MainObjectiveBasicRead
from app.schemas.municipality_schema import MunicipalityRead
from app.schemas.user_schema import UserRead
