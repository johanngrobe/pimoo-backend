from pydantic import BaseModel, ConfigDict, field_serializer
from typing import List, Optional
from datetime import datetime, date
from uuid import UUID
from .mobility_result import MobilityResultOut
from .user import UserRead

class MobilitySubmissionBase(BaseModel):
    label: str
    desc: str
    administration_no: str
    administration_date: date
    is_published: bool = False

class MobilitySubmissionCreate(MobilitySubmissionBase):
    pass

class MobilitySubmissionUpdate(BaseModel):
    label: Optional[str] = None
    desc: Optional[str] = None
    administration_no: Optional[str] = None
    administration_date: Optional[date] = None
    is_published: Optional[bool] = None

class MobilitySubmissionOut(MobilitySubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    objectives: List[MobilityResultOut]
    created_at: datetime
    municipality_id: int
    author: Optional[UserRead] = None
    last_editor: Optional[UserRead] = None


    @field_serializer('objectives')
    def sort_main_objectives(self, objectives: List["MobilityResultOut"]) -> List["MobilityResultOut"]:
        # Ensure sorting of the list by sub_objective.no
        return sorted(objectives, key=lambda x: x.main_objective.no)
    

class MobilitySubmissionFilter(BaseModel):
    is_published: Optional[bool] = None
    by_user_id: Optional[bool] = False
    by_user_role: Optional[bool] = None
