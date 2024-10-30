from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from .municipality import MunicipalityOut
from .user import UserRead

class TagBase(BaseModel):
    label: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    label: Optional[str] = None

class TagOut(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    municipality_id: int
    municipality: MunicipalityOut
    author: Optional[UserRead] = None
    last_editor: Optional[UserRead] = None
