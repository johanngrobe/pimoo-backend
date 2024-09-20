from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .tag import TagOut

class TextBlockBase(BaseModel):
    label: str
    

class TextBlockCreate(TextBlockBase):
    tag_ids: Optional[List[int]] = []

class TextBlockOut(TextBlockBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: Optional[List[TagOut]] = []