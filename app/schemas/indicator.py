from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .tag import TagOut
from uuid import UUID
from .user import UserRead

class IndicatorBase(BaseModel):
    label: str
    source_url: Optional[str] = None
    

class IndicatorCreate(IndicatorBase):
    tag_ids: Optional[List[int]] = []

class IndicatorAdd(BaseModel):
    id: int

class IndicatorUpdate(BaseModel):
    label: Optional[str] = None
    source_url: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class IndicatorOut(IndicatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: Optional[List[TagOut]] = []
    municipality_id: int
    author: Optional[UserRead] = None
    last_editor: Optional[UserRead] = None

