from pydantic import BaseModel, ConfigDict, field_serializer
from typing import List, Optional
from datetime import datetime, date
from .mobility_result import MobilityResultOut

class MobilitySubmissionBase(BaseModel):
    label: str
    author: str
    desc: str
    administration_no: str
    administration_date: date
    # municipality_id: int

class MobilitySubmissionCreate(MobilitySubmissionBase):
    pass

class MobilitySubmissionOut(MobilitySubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    objectives: List["MobilityResultOut"]
    created_at: datetime

    @field_serializer('objectives')
    def sort_main_objectives(self, objectives: List["MobilityResultOut"]) -> List["MobilityResultOut"]:
        # Ensure sorting of the list by sub_objective.no
        return sorted(objectives, key=lambda x: x.main_objective.no)
