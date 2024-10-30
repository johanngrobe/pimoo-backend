from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from .tag import TagOut
from .municipality import MunicipalityOut
from .user import UserRead

class TextBlockBase(BaseModel):
    label: str

class TextBlockCreate(TextBlockBase):
    tag_ids: Optional[List[int]] = []

class TextBlockUpdate(BaseModel):
    label: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class TextBlockOut(TextBlockBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tags: Optional[List[TagOut]] = []
    municipality_id: int
    municipality: MunicipalityOut
    author: Optional[UserRead] = None
    last_editor: Optional[UserRead] = None