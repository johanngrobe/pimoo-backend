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


class KlimacheckEingabeBase(BaseModel):
    """
    Base schema for KlimacheckEingabe, shared by create and update schemas.
    Holds the primary fields related to the climate submission data.
    """

    verwaltungsvorgang_nr: str = Field(
        ..., description="Internal tracking number assigned by the administration."
    )
    verwaltungsvorgang_datum: date = Field(
        ..., description="Date the submission was registered by the administration."
    )
    name: str = Field(
        ..., description="Short descriptive title or label for the submission."
    )
    klimarelevanz: ImpactEnum = Field(
        ...,
        description="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    auswirkung_thg: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Estimated greenhouse gas impact, ranging from -3 to 3.",
    )
    auswirkung_klimaanpassung: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Level of impact on climate adaptation, ranging from -3 to 3.",
    )
    auswirkung_beschreibung: Optional[str] = Field(
        None, description="Detailed description of the anticipated climate impact."
    )
    auswirkung_dauer: Optional[ImpactDurationEnum] = Field(
        None, description="Duration of the impact (short, medium, long)."
    )
    alternativen: Optional[str] = Field(
        None, description="Description of any considered alternatives to the project."
    )
    veroeffentlicht: bool = Field(
        False,
        description="Indicates if the submission is published and visible to others.",
    )


class KlimacheckEingabeCreate(KlimacheckEingabeBase):
    """
    Schema for creating a new KlimacheckEingabe entry.
    Inherits all fields from KlimacheckEingabeBase.
    """

    pass


class KlimacheckEingabeUpdate(BaseModel):
    """
    Schema for updating a KlimacheckEingabe entry.
    All fields are optional to allow partial updates.
    """

    verwaltungsvorgang_nr: Optional[str] = Field(
        None, description="Internal tracking number assigned by the administration."
    )
    verwaltungsvorgang_datum: Optional[date] = Field(
        None, description="Date the submission was registered by the administration."
    )
    name: Optional[str] = Field(
        None, description="Short descriptive title or label for the submission."
    )
    klimarelevanz: Optional[ImpactEnum] = Field(
        None,
        description="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    auswirkung_thg: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Estimated greenhouse gas impact, ranging from -3 to 3.",
    )
    auswirkung_klimaanpassung: Optional[int] = Field(
        None,
        ge=-3,
        le=3,
        description="Level of impact on climate adaptation, ranging from -3 to 3.",
    )
    auswirkung_beschreibung: Optional[str] = Field(
        None, description="Detailed description of the anticipated climate impact."
    )
    auswirkung_dauer: Optional[ImpactDurationEnum] = Field(
        None, description="Duration of the impact (short, medium, long)."
    )
    alternativen: Optional[str] = Field(
        None, description="Description of any considered alternatives to the project."
    )
    veroeffentlicht: Optional[bool] = Field(
        None,
        description="Indicates if the submission is published and visible to others.",
    )


class KlimacheckEingabeRead(KlimacheckEingabeBase):
    """
    Schema for returning a KlimacheckEingabe with extra metadata fields.
    Includes fields for author and editor details as well as translated labels.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for each climate submission.")
    erstellt_am: datetime = Field(..., description="Timestamp of submission creation.")
    gemeinde_id: int = Field(
        ..., description="Foreign key to the associated municipality."
    )
    autor: Optional[UserRead] = Field(
        None, description="User who created the submission."
    )
    letzter_bearbeiter: Optional[UserRead] = Field(
        None, description="User who last edited the submission."
    )

    # Computed labels for user-friendly display
    klimarelevanz_label: Optional[str] = Field(
        None, description="Human-readable label for the climate impact."
    )
    auswirkung_thg_label: Optional[str] = Field(
        None, description="Human-readable label for greenhouse gas impact."
    )
    auswirkung_klimaanpassung_label: Optional[str] = Field(
        None, description="Human-readable label for climate adaptation impact."
    )
    auswirkung_dauer_label: Optional[str] = Field(
        None, description="Human-readable label for the duration of impact."
    )

    # Serializer methods to add human-readable labels
    @field_serializer("klimarelevanz_label", when_used="json")
    def serialize_impact_label(self, _):
        """Provides a user-friendly label for the climate impact."""
        return label_climate_impact(self.klimarelevanz)

    @field_serializer("auswirkung_thg_label", when_used="json")
    def serialize_impact_ghg_label(self, _):
        """Provides a user-friendly label for greenhouse gas impact."""
        return label_climate_impact_ghg(self.auswirkung_thg)

    @field_serializer("auswirkung_klimaanpassung_label", when_used="json")
    def serialize_impact_adaption_label(self, _):
        """Provides a user-friendly label for climate adaptation impact."""
        return label_climate_impact_ghg(self.auswirkung_klimaanpassung)

    @field_serializer("auswirkung_dauer_label", when_used="json")
    def serialize_impact_duration_label(self, _):
        """Provides a user-friendly label for the duration of impact."""
        return label_climate_impact_duration(self.auswirkung_dauer)


class KlimacheckEingabeFilter(BaseModel):
    """
    Schema for filtering KlimacheckEingabe records based on criteria.
    """

    veroeffentlicht: Optional[bool] = Field(
        None, description="Filter by publication status."
    )
    user_id: Optional[bool] = Field(
        False, description="Filter submissions by the current user's ID."
    )
    user_rolle: Optional[bool] = Field(
        None, description="Filter submissions based on the user's role."
    )
