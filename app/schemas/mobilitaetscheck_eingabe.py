from typing import List, Optional

from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class MobilitaetscheckEingabeBase(BaseModel):
    """
    Base schema for a mobility submission, containing core attributes.
    """

    name: str = Field(
        ..., description="A descriptive title for the mobility submission."
    )
    beschreibung: str = Field(
        ..., description="Detailed description of the submission."
    )
    verwaltungsvorgang_nr: str = Field(
        ..., description="Internal tracking number assigned by the administration."
    )
    verwaltungsvorgang_datum: date = Field(
        ..., description="Date when the submission was registered."
    )
    veroeffentlicht: bool = Field(
        False,
        description="Indicates if the submission is published and visible to others.",
    )


class MobilitaetscheckEingabeCreate(MobilitaetscheckEingabeBase):
    """
    Schema for creating a new mobility submission.
    Inherits fields from MobilitaetscheckEingabeBase.
    """

    pass


class MobilitaetscheckEingabeUpdate(BaseModel):
    """
    Schema for updating an existing mobility submission. Allows partial updates.
    """

    name: Optional[str] = Field(None, description="Updated title for the submission.")
    beschreibung: Optional[str] = Field(
        None, description="Updated description of the submission."
    )
    verwaltungsvorgang_nr: Optional[str] = Field(
        None, description="Updated tracking number from the administration."
    )
    verwaltungsvorgang_datum: Optional[date] = Field(
        None, description="Updated date of submission registration."
    )
    veroeffentlicht: Optional[bool] = Field(
        None, description="Updated publication status of the submission."
    )


class MobilitaetscheckEingabeRead(MobilitaetscheckEingabeBase):
    """
    Detailed read schema for a mobility submission, including objectives and metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the submission.")
    ziel_ober: List["MobilitaetscheckEingabeZielOberRead"] = Field(
        default_factory=list,
        description="List of mobility results associated with the submission.",
    )
    erstellt_am: datetime = Field(
        ..., description="Timestamp of when the submission was created."
    )
    gemeinde_id: int = Field(
        ..., description="ID of the municipality associated with the submission."
    )
    autor: Optional["UserRead"] = Field(
        None, description="User who created the submission."
    )
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the submission."
    )

    @field_serializer("ziel_ober")
    def sort_main_objectives(
        self, ziel_ober: List["MobilitaetscheckEingabeZielOberRead"]
    ) -> List["MobilitaetscheckEingabeZielOberRead"]:
        """
        Sorts the list of objectives by the main objective number.
        """
        return sorted(ziel_ober, key=lambda x: x.ziel_ober.nr)


class MobilitaetscheckEingabeFilter(BaseModel):
    """
    Schema for filtering mobility submissions based on various criteria.
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


# Late imports for forward references
from app.schemas.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOberRead,
)
from app.schemas.user import UserRead
