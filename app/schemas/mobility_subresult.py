from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.utils.enum_util import SpatialImpactEnum


class MobilitySubResultBase(BaseModel):
    """
    Base schema for a mobility sub-result, linking it to a sub-objective and including impact details.
    """

    mobility_result_id: int = Field(
        ..., description="ID of the related mobility result."
    )
    sub_objective_id: int = Field(
        ..., description="ID of the associated sub-objective."
    )
    target: Optional[bool] = Field(
        None, description="Indicates if the target was achieved."
    )
    impact: Optional[int] = Field(
        None, ge=-3, le=3, description="Impact score, ranging from -3 to 3."
    )
    spatial_impact: Optional[SpatialImpactEnum] = Field(
        None, description="Type of spatial impact."
    )
    annotation: Optional[str] = Field(
        None, description="Additional notes or comments about the result."
    )


class MobilitySubResultCreate(MobilitySubResultBase):
    """
    Schema for creating a new mobility sub-result, including associated indicator IDs.
    """

    indicator_ids: Optional[List[int]] = Field(
        default_factory=list, description="List of associated indicator IDs."
    )


class MobilitySubResultUpdate(BaseModel):
    """
    Schema for updating an existing mobility sub-result. All fields are optional for partial updates.
    """

    target: Optional[bool] = Field(None, description="Updated target status.")
    impact: Optional[int] = Field(
        None, ge=-3, le=3, description="Updated impact score, ranging from -3 to 3."
    )
    spatial_impact: Optional[SpatialImpactEnum] = Field(
        None, description="Updated spatial impact type."
    )
    annotation: Optional[str] = Field(None, description="Updated notes or comments.")
    indicator_ids: Optional[List[int]] = Field(
        None, description="Updated list of associated indicator IDs."
    )


class MobilitySubResultRead(MobilitySubResultBase):
    """
    Detailed read schema for a mobility sub-result, including sub-objective and indicator details.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the mobility sub-result.")
    sub_objective: "SubObjectiveBasicRead" = Field(
        ..., description="The associated sub-objective details."
    )
    indicators: Optional[List["IndicatorBasicRead"]] = Field(
        default_factory=list, description="List of associated indicators."
    )

    # Field serializer to return only the list of IDs from indicators
    @field_serializer("indicators")
    def serialize_indicators(self, indicators: List["IndicatorBasicRead"]) -> List[int]:
        """
        Serializer to extract and return only the IDs of associated indicators.
        """
        return [indicator.id for indicator in indicators]


# Late imports for forward references
from app.schemas.indicator import IndicatorBasicRead
from app.schemas.sub_objective import SubObjectiveBasicRead
