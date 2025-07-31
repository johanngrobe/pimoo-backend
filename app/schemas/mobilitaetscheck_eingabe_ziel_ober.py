from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class MobilitaetscheckEingabeZielOberBase(BaseModel):
    """
    Base schema for a mobility result, linking submissions and objectives.
    """

    eingabe_id: int = Field(..., description="ID of the related submission.")
    ziel_ober_id: int = Field(
        ..., description="ID of the main objective associated with this result."
    )
    tangiert: Optional[bool] = Field(
        False, description="Indicates whether the target was met for this objective."
    )


class MobilitaetscheckEingabeZielOberCreate(MobilitaetscheckEingabeZielOberBase):
    """
    Schema for creating a new mobility result.
    """

    pass


class MobilitaetscheckEingabeZielOberUpdate(BaseModel):
    """
    Schema for updating an existing mobility result. Allows partial updates.
    """

    tangiert: Optional[bool] = Field(
        None, description="Updated target status for the objective."
    )


class MobilitaetscheckEingabeZielOberRead(MobilitaetscheckEingabeZielOberBase):
    """
    Detailed read schema for a mobility result, including related main objective and sorted sub-objectives.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the mobility result.")
    ziel_ober: "MobilitaetscheckZielOberBaseRead" = Field(
        ..., description="Basic information about the related main objective."
    )
    eingabe_ziel_unter: List["MobilitaetscheckEingabeZielUnterRead"] = Field(
        default_factory=list,
        description="List of sub-objective results, sorted by sub-objective number.",
    )

    # Apply a field serializer to sort sub_objectives by sub_objective.no
    @field_serializer("eingabe_ziel_unter")
    def sort_sub_objectives(
        self, eingabe_ziel_unter: List["MobilitaetscheckEingabeZielUnterRead"]
    ) -> List["MobilitaetscheckEingabeZielUnterRead"]:
        """
        Sorts the list of sub-objectives by the 'no' attribute of each sub-objective.
        """
        return sorted(eingabe_ziel_unter, key=lambda x: x.ziel_unter.nr)


# Late imports for forward references
from app.schemas.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOberBaseRead
from app.schemas.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnterRead,
)
