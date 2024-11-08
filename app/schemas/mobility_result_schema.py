from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class MobilityResultBase(BaseModel):
    """
    Base schema for a mobility result, linking submissions and objectives.
    """

    submission_id: int = Field(..., description="ID of the related submission.")
    main_objective_id: int = Field(
        ..., description="ID of the main objective associated with this result."
    )
    target: bool = Field(
        ..., description="Indicates whether the target was met for this objective."
    )


class MobilityResultCreate(MobilityResultBase):
    """
    Schema for creating a new mobility result.
    """

    pass


class MobilityResultUpdate(BaseModel):
    """
    Schema for updating an existing mobility result. Allows partial updates.
    """

    target: Optional[bool] = Field(
        None, description="Updated target status for the objective."
    )


class MobilityResultRead(MobilityResultBase):
    """
    Detailed read schema for a mobility result, including related main objective and sorted sub-objectives.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the mobility result.")
    main_objective: "MainObjectiveBasicRead" = Field(
        ..., description="Basic information about the related main objective."
    )
    sub_objectives: List["MobilitySubResultRead"] = Field(
        default_factory=list,
        description="List of sub-objective results, sorted by sub-objective number.",
    )

    # Apply a field serializer to sort sub_objectives by sub_objective.no
    @field_serializer("sub_objectives")
    def sort_sub_objectives(
        self, sub_objectives: List["MobilitySubResultRead"]
    ) -> List["MobilitySubResultRead"]:
        """
        Sorts the list of sub-objectives by the 'no' attribute of each sub-objective.
        """
        return sorted(sub_objectives, key=lambda x: x.sub_objective.no)


# Late imports for forward references
from app.schemas.main_objective_schema import MainObjectiveBasicRead
from app.schemas.mobility_subresult_schema import MobilitySubResultRead
