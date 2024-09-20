from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .tag import TagOut

class IndicatorBase(BaseModel):
    label: str
    

class IndicatorCreate(IndicatorBase):
    tag_ids: Optional[List[int]] = []

class IndicatorAdd(BaseModel):
    id: int

class IndicatorOut(IndicatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: Optional[List[TagOut]] = []
