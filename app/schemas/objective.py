from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from .municipality import MunicipalityOut
from .user import UserRead

class MainObjectiveBase(BaseModel):
    no: int
    label: str

class MainObjectiveCreate(MainObjectiveBase):
    pass

class MainObjectiveUpdate(BaseModel):
    no: Optional[int] = None
    label: Optional[str] = None

class MainObjectiveOut(MainObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    municipality_id: int
    sub_objectives: Optional[List["SubObjectiveOut"]]
    municipality: MunicipalityOut
    author: Optional["UserRead"]
    last_editor: Optional["UserRead"]

class MainObjectiveOutForResult(MainObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class SubObjectiveBase(MainObjectiveBase):
    main_objective_id: int
    label: str
    no: int


class SubObjectiveCreate(SubObjectiveBase):
    pass

class SubObjectiveUpdate(BaseModel):
    no: Optional[int] = None
    label: Optional[str] = None
    main_objective_id: Optional[int] = None

class SubObjectiveOut(SubObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    municipality_id: int

class SubObjectiveOutDetail(SubObjectiveBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    main_objective: MainObjectiveOutForResult
    municipality_id: int
    municipality: MunicipalityOut
    author: Optional["UserRead"] = None
    last_editor: Optional["UserRead"] = None