from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from typing import List, Optional
from .indicator import IndicatorOut
from .objective import MainObjectiveOutForResult, SubObjectiveOut

class MobilityResultBase(BaseModel):
    submission_id: int
    main_objective_id: int
    target: bool

class MobilityResultCreate(MobilityResultBase):
    pass

class MobilityResultUpdate(BaseModel):
    target: Optional[bool] = None


class MobilityResultOut(MobilityResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    main_objective: MainObjectiveOutForResult
    sub_objectives: List["MobilitySubResultOut"]

    # Apply a field serializer to sort sub_objectives by sub_objective.no
    @field_serializer('sub_objectives')
    def sort_sub_objectives(self, sub_objectives: List["MobilitySubResultOut"]) -> List["MobilitySubResultOut"]:
        # Ensure sorting of the list by sub_objective.no
        return sorted(sub_objectives, key=lambda x: x.sub_objective.no)


class MobilitySubResultBase(BaseModel):
    mobility_result_id: int
    sub_objective_id: int
    target: Optional[bool] = None
    impact: Optional[int] = None
    spatial_impact: Optional[str] = None
    annotation: Optional[str] = None
    

class MobilitySubResultCreate(MobilitySubResultBase):
    indicator_ids: Optional[List[int]] = []

class MobilitySubResultUpdate(BaseModel):
    target: Optional[bool] = None
    impact: Optional[int] = None
    spatial_impact: Optional[str] = None
    annotation: Optional[str] = None
    indicator_ids: Optional[List[int]] = None

class MobilitySubResultOut(MobilitySubResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sub_objective: SubObjectiveOut
    indicators: Optional[List["IndicatorOut"]] = []

    # Field serializer to return only the list of ids from indicators
    @field_serializer('indicators')
    def serialize_indicators(self, indicators):
        return [indicator.id for indicator in indicators]
