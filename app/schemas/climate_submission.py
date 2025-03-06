from typing import Optional

from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from app.utils.enum_util import ImpactEnum, ImpactDurationEnum
from app.utils.label_util import (
    label_climate_impact,
    label_climate_impact_ghg,
    label_climate_impact_duration,
)
from app.schemas.user import UserRead


class ClimateSubmissionBase(BaseModel):
    """
    Base schema for ClimateSubmission, shared by create and update schemas.
    Holds the primary fields related to the climate submission data.
    """

    administration_no: str = Field(
        ..., description="Internal tracking number assigned by the administration."
    )
    administration_date: date = Field(
        ..., description="Date the submission was registered by the administration."
    )
    label: str = Field(
        ..., description="Short descriptive title or label for the submission."
    )
    impact: ImpactEnum = Field(
        ...,
        description="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    impact_ghg: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Estimated greenhouse gas impact, ranging from -3 to 3.",
    )
    impact_adaption: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Level of impact on climate adaptation, ranging from -3 to 3.",
    )
    impact_desc: Optional[str] = Field(
        None, description="Detailed description of the anticipated climate impact."
    )
    impact_duration: Optional[ImpactDurationEnum] = Field(
        None, description="Duration of the impact (short, medium, long)."
    )
    alternative_desc: Optional[str] = Field(
        None, description="Description of any considered alternatives to the project."
    )
    is_published: bool = Field(
        False,
        description="Indicates if the submission is published and visible to others.",
    )


class ClimateSubmissionCreate(ClimateSubmissionBase):
    """
    Schema for creating a new ClimateSubmission entry.
    Inherits all fields from ClimateSubmissionBase.
    """

    pass


class ClimateSubmissionUpdate(BaseModel):
    """
    Schema for updating a ClimateSubmission entry.
    All fields are optional to allow partial updates.
    """

    administration_no: Optional[str] = Field(
        None, description="Internal tracking number assigned by the administration."
    )
    administration_date: Optional[date] = Field(
        None, description="Date the submission was registered by the administration."
    )
    label: Optional[str] = Field(
        None, description="Short descriptive title or label for the submission."
    )
    impact: Optional[ImpactEnum] = Field(
        None,
        description="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    impact_ghg: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Estimated greenhouse gas impact, ranging from -3 to 3.",
    )
    impact_adaption: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Level of impact on climate adaptation, ranging from -3 to 3.",
    )
    impact_desc: Optional[str] = Field(
        None, description="Detailed description of the anticipated climate impact."
    )
    impact_duration: Optional[ImpactDurationEnum] = Field(
        None, description="Duration of the impact (short, medium, long)."
    )
    alternative_desc: Optional[str] = Field(
        None, description="Description of any considered alternatives to the project."
    )
    is_published: Optional[bool] = Field(
        None,
        description="Indicates if the submission is published and visible to others.",
    )


class ClimateSubmissionRead(ClimateSubmissionBase):
    """
    Schema for returning a ClimateSubmission with extra metadata fields.
    Includes fields for author and editor details as well as translated labels.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for each climate submission.")
    created_at: datetime = Field(..., description="Timestamp of submission creation.")
    municipality_id: int = Field(
        ..., description="Foreign key to the associated municipality."
    )
    author: Optional[UserRead] = Field(
        None, description="User who created the submission."
    )
    last_editor: Optional[UserRead] = Field(
        None, description="User who last edited the submission."
    )

    # Computed labels for user-friendly display
    impact_label: Optional[str] = Field(
        None, description="Human-readable label for the climate impact."
    )
    impact_ghg_label: Optional[str] = Field(
        None, description="Human-readable label for greenhouse gas impact."
    )
    impact_adaption_label: Optional[str] = Field(
        None, description="Human-readable label for climate adaptation impact."
    )
    impact_duration_label: Optional[str] = Field(
        None, description="Human-readable label for the duration of impact."
    )

    # Serializer methods to add human-readable labels
    @field_serializer("impact_label", when_used="json")
    def serialize_impact_label(self, _):
        """Provides a user-friendly label for the climate impact."""
        return label_climate_impact(self.impact)

    @field_serializer("impact_ghg_label", when_used="json")
    def serialize_impact_ghg_label(self, _):
        """Provides a user-friendly label for greenhouse gas impact."""
        return label_climate_impact_ghg(self.impact_ghg)

    @field_serializer("impact_adaption_label", when_used="json")
    def serialize_impact_adaption_label(self, _):
        """Provides a user-friendly label for climate adaptation impact."""
        return label_climate_impact_ghg(self.impact_adaption)

    @field_serializer("impact_duration_label", when_used="json")
    def serialize_impact_duration_label(self, _):
        """Provides a user-friendly label for the duration of impact."""
        return label_climate_impact_duration(self.impact_duration)


class ClimateSubmissionFilter(BaseModel):
    """
    Schema for filtering ClimateSubmission records based on criteria.
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
