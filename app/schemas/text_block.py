from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TextBlockBase(BaseModel):
    label: str
    tags: Optional[List[int]]

class TextBlockCreate(TextBlockBase):
    pass

class TextBlockOut(TextBlockBase):
    model_config = ConfigDict(from_attributes=True)

    id: int