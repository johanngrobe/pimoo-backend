from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from .mobility_result import MobilityResultOut

class MobilitySubmissionBase(BaseModel):
    label: str
    author: str
    desc: str
    administration_no: str
    administration_date: date

class MobilitySubmissionCreate(MobilitySubmissionBase):
    pass

class MobilitySubmissionOut(MobilitySubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    objectives: List["MobilityResultOut"]
    created_at: datetime