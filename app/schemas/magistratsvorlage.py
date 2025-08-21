from typing import List, Optional

from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_serializer, computed_field


class MagistratsvorlageBase(BaseModel):
    """
    Base schema for a mobility submission, containing core attributes.
    """

    name: str = Field(
        ..., description="A descriptive title for the mobility submission."
    )
    beschreibung: Optional[str] = Field(
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


class MagistratsvorlageCreate(MagistratsvorlageBase):
    """
    Schema for creating a new mobility submission.
    Inherits fields from MobilitaetscheckEingabeBase.
    """

    gemeinde_gebiet_ids: Optional[List[int]] = Field(
        None, description="Liste der IDs der zugeordneten Gemeindegebiete."
    )


class MagistratsvorlageUpdate(BaseModel):
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
    gemeinde_gebiet_ids: Optional[List[int]] = Field(
        None, description="Liste der IDs der zugeordneten Gemeindegebiete."
    )


class MagistratsvorlageBaseRead(MagistratsvorlageBase):
    """
    Detailed read schema for a mobility submission, including objectives and metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the submission.")

    erstellt_am: datetime = Field(
        ..., description="Timestamp of when the submission was created."
    )


class MagistratsvorlageRead(MagistratsvorlageBaseRead):
    mobilitaetschecks: Optional[List["MobilitaetscheckEingabeBaseRead"]] = Field(
        ...,
        description="List of mobility results associated with the submission.",
    )
    klimachecks: Optional[List["KlimacheckEingabeRead"]] = Field(
        ...,
        description="List of climate checks associated with the submission.",
    )
    gemeinde_gebiete: Optional[List["GemeindeGebietRead"]] = Field(
        default_factory=list,
        description="List of associated municipal areas.",
    )

    @computed_field
    @property
    def gemeinde_gebiet_ids(self) -> List[int]:
        """
        Automatically computes the list of tag IDs from the tags.
        """
        return [gebiet.id for gebiet in self.gemeinde_gebiete or []]


from app.schemas.gemeinde_gebiet import GemeindeGebietRead
from app.schemas.mobilitaetscheck_eingabe import MobilitaetscheckEingabeBaseRead
from app.schemas.klimacheck_eingabe import KlimacheckEingabeRead
