from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MainObjectiveBase(BaseModel):
    no: int
    label: str
    # municipality_id: int

class MainObjectiveCreate(MainObjectiveBase):
    pass

class MainObjectiveOut(MainObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sub_objectives: Optional[List["SubObjectiveOut"]]

class MainObjectiveOutForResult(MainObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class SubObjectiveBase(MainObjectiveBase):
    main_objective_id: int
    # municipality_id: int

class SubObjectiveCreate(SubObjectiveBase):
    pass

class SubObjectiveOut(SubObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class SubObjectiveOutDetail(SubObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    main_objective: MainObjectiveOutForResult