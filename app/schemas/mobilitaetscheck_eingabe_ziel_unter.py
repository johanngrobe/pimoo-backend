from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.enum_util import SpatialImpactEnum


class MobilitaetscheckEingabeZielUnterBase(BaseModel):
    """
    Base schema for a mobility sub-result, linking it to a sub-objective and including impact details.
    """

    eingabe_ziel_ober_id: int = Field(
        ..., description="ID of the related mobility result."
    )
    ziel_unter_id: int = Field(..., description="ID of the associated sub-objective.")
    tangiert: Optional[bool] = Field(
        False, description="Indicates if the target was achieved."
    )
    auswirkung: Optional[int] = Field(
        None, ge=-3, le=3, description="Impact score, ranging from -3 to 3."
    )
    auswirkung_raeumlich: Optional[SpatialImpactEnum] = Field(
        None, description="Type of spatial impact."
    )
    anmerkung: Optional[str] = Field(
        None, description="Additional notes or comments about the result."
    )


class MobilitaetscheckEingabeZielUnterCreate(MobilitaetscheckEingabeZielUnterBase):
    """
    Schema for creating a new mobility sub-result, including associated indicator IDs.
    """

    indikator_ids: Optional[List[int]] = Field(
        default_factory=list, description="List of associated indicator IDs."
    )


class MobilitaetscheckEingabeZielUnterUpdate(BaseModel):
    """
    Schema for updating an existing mobility sub-result. All fields are optional for partial updates.
    """

    tangiert: Optional[bool] = Field(None, description="Updated target status.")
    auswirkung: Optional[int] = Field(
        None, ge=-3, le=3, description="Updated impact score, ranging from -3 to 3."
    )
    auswirkung_raeumlich: Optional[SpatialImpactEnum] = Field(
        None, description="Updated spatial impact type."
    )
    anmerkung: Optional[str] = Field(None, description="Updated notes or comments.")
    indikator_ids: Optional[List[int]] = Field(
        None, description="Updated list of associated indicator IDs."
    )


class MobilitaetscheckEingabeZielUnterRead(MobilitaetscheckEingabeZielUnterBase):
    """
    Detailed read schema for a mobility sub-result, including sub-objective and indicator details.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the mobility sub-result.")
    ziel_unter: "MobilitaetscheckZielUnterBaseRead" = Field(
        ..., description="The associated sub-objective details."
    )
    indikatoren: Optional[List["IndikatorBaseRead"]] = Field(
        default_factory=list, description="List of associated indicators."
    )

    # Field serializer to return only the list of IDs from indicators
    @field_serializer("indikatoren")
    def serialize_indicators(self, indikatoren: List["IndikatorBaseRead"]) -> List[int]:
        """
        Serializer to extract and return only the IDs of associated indicators.
        """
        return [indikator.id for indikator in indikatoren]


# Late imports for forward references
from app.schemas.indikator import IndikatorBaseRead
from app.schemas.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnterBaseRead
