from typing import List, Optional

from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class MobilitySubmissionBase(BaseModel):
    """
    Base schema for a mobility submission, containing core attributes.
    """

    label: str = Field(
        ..., description="A descriptive title for the mobility submission."
    )
    desc: str = Field(..., description="Detailed description of the submission.")
    administration_no: str = Field(
        ..., description="Internal tracking number assigned by the administration."
    )
    administration_date: date = Field(
        ..., description="Date when the submission was registered."
    )
    is_published: bool = Field(
        False,
        description="Indicates if the submission is published and visible to others.",
    )


class MobilitySubmissionCreate(MobilitySubmissionBase):
    """
    Schema for creating a new mobility submission.
    Inherits fields from MobilitySubmissionBase.
    """

    pass


class MobilitySubmissionUpdate(BaseModel):
    """
    Schema for updating an existing mobility submission. Allows partial updates.
    """

    label: Optional[str] = Field(None, description="Updated title for the submission.")
    desc: Optional[str] = Field(
        None, description="Updated description of the submission."
    )
    administration_no: Optional[str] = Field(
        None, description="Updated tracking number from the administration."
    )
    administration_date: Optional[date] = Field(
        None, description="Updated date of submission registration."
    )
    is_published: Optional[bool] = Field(
        None, description="Updated publication status of the submission."
    )


class MobilitySubmissionRead(MobilitySubmissionBase):
    """
    Detailed read schema for a mobility submission, including objectives and metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the submission.")
    objectives: List["MobilityResultRead"] = Field(
        default_factory=list,
        description="List of mobility results associated with the submission.",
    )
    created_at: datetime = Field(
        ..., description="Timestamp of when the submission was created."
    )
    municipality_id: int = Field(
        ..., description="ID of the municipality associated with the submission."
    )
    author: Optional["UserRead"] = Field(
        None, description="User who created the submission."
    )
    last_editor: Optional["UserRead"] = Field(
        None, description="User who last edited the submission."
    )

    @field_serializer("objectives")
    def sort_main_objectives(
        self, objectives: List["MobilityResultRead"]
    ) -> List["MobilityResultRead"]:
        """
        Sorts the list of objectives by the main objective number.
        """
        return sorted(objectives, key=lambda x: x.main_objective.no)


class MobilitySubmissionFilter(BaseModel):
    """
    Schema for filtering mobility submissions based on various criteria.
    """

    is_published: Optional[bool] = Field(
        None, description="Filter by publication status."
    )
    by_user_id: Optional[bool] = Field(
        False, description="Filter submissions by the current user's ID."
    )
    by_user_role: Optional[bool] = Field(
        None, description="Filter submissions based on the user's role."
    )


# Late imports for forward references
from app.schemas.mobility_result_schema import MobilityResultRead
from app.schemas.user_schema import UserRead
