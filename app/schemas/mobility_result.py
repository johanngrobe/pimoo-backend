from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .indicator import IndicatorOut
from .objective import MainObjectiveOutForResult, SubObjectiveOut

class MobilityResultBase(BaseModel):
    submission_id: int
    main_objective_id: int
    target: bool

class MobilityResultCreate(MobilityResultBase):
    pass

class MobilityResultOut(MobilityResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    main_objective: MainObjectiveOutForResult
    sub_objectives: List["MobilitySubResultOut"]

class MobilitySubResultBase(BaseModel):
    mobility_result_id: int
    sub_objective_id: int
    target: Optional[bool] = None
    impact: Optional[int] = None
    spatial_impact: Optional[str] = None
    annotation: Optional[str] = None
    

class MobilitySubResultCreate(MobilitySubResultBase):
    indicator_ids: Optional[List[int]] = []

class MobilitySubResultOut(MobilitySubResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sub_objective: SubObjectiveOut
    indicators: Optional[List["IndicatorOut"]] = []