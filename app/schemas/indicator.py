from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class IndicatorBase(BaseModel):
    label: str
    tags: Optional[List[int]]

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorAdd(BaseModel):
    id: int

class IndicatorOut(IndicatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
