from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TagBase(BaseModel):
    label: str

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
