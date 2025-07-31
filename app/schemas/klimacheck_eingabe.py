from typing import Optional

from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from app.utils.label_util import (
    label_klimacheck_auswirkung,
)
from app.schemas.user import UserRead


class KlimacheckEingabeBase(BaseModel):
    """
    Base schema for KlimacheckEingabe, shared by create and update schemas.
    Holds the primary fields related to the climate submission data.
    """

    name: Optional[str] = Field(None, description="Name of the climate submission.")
    magistratsvorlage_id: Optional[int] = Field(
        None, description="ID of the associated magistrate submission."
    )
    klimarelevanz_id: int = Field(
        ...,
        description="Estimated impact on climate (e.g., positive, negative, no effect).",
    )
    auswirkung_thg: Optional[int] = Field(
        None,
        ge=-2,
        le=2,
        description="Estimated greenhouse gas impact, ranging from -3 to 3.",
    )
    auswirkung_klimaanpassung: Optional[int] = Field(
        None,
        ge=-2,
        le=2,
        description="Level of impact on climate adaptation, ranging from -3 to 3.",
    )
    auswirkung_beschreibung: Optional[str] = Field(
        None, description="Detailed description of the anticipated climate impact."
    )
    auswirkung_dauer_id: Optional[int] = Field(
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

    name: Optional[str] = Field(
        None, description="Updated name of the climate submission."
    )
    klimarelevanz_id: Optional[int] = Field(
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
    auswirkung_dauer_id: Optional[int] = Field(
        None, description="Duration of the impact (short, medium, long)."
    )
    alternativen: Optional[str] = Field(
        None, description="Description of any considered alternatives to the project."
    )
    veroeffentlicht: Optional[bool] = Field(
        None,
        description="Indicates if the submission is published and visible to others.",
    )


class KlimacheckEingabeBaseRead(KlimacheckEingabeBase):
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
    klimarelevanz: Optional["KlimacheckKlimarelevanzRead"] = Field(
        None, description="Human-readable label for the climate impact."
    )
    auswirkung_thg_label: Optional[str] = Field(
        None, description="Human-readable label for greenhouse gas impact."
    )
    auswirkung_klimaanpassung_label: Optional[str] = Field(
        None, description="Human-readable label for climate adaptation impact."
    )
    auswirkung_dauer: Optional["KlimacheckAuswirkungDauerRead"] = Field(
        None, description="Human-readable label for the duration of impact."
    )

    @field_serializer("auswirkung_thg_label", when_used="json")
    def serialize_impact_ghg_label(self, _):
        """Provides a user-friendly label for greenhouse gas impact."""
        return label_klimacheck_auswirkung(self.auswirkung_thg)

    @field_serializer("auswirkung_klimaanpassung_label", when_used="json")
    def serialize_impact_adaption_label(self, _):
        """Provides a user-friendly label for climate adaptation impact."""
        return label_klimacheck_auswirkung(self.auswirkung_klimaanpassung)


class KlimacheckEingabeRead(KlimacheckEingabeBaseRead):

    magistratsvorlage: Optional["MagistratsvorlageBaseRead"] = Field(
        None, description="Associated magistrate submission details."
    )


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


from app.schemas.klimacheck_auswirkung_dauer import KlimacheckAuswirkungDauerRead
from app.schemas.klimacheck_klimarelevanz import KlimacheckKlimarelevanzRead
from app.schemas.magistratsvorlage import MagistratsvorlageBaseRead
