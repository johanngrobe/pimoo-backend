from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class TextblockBase(BaseModel):
    """
    Base schema for a text block, containing a label.
    """

    name: str = Field(..., description="The label or title for the text block.")


class TextblockCreate(TextblockBase):
    """
    Schema for creating a new text block, including optional associated tag IDs.
    """

    tag_ids: Optional[List[int]] = Field(
        default_factory=list, description="List of associated tag IDs."
    )


class TextblockUpdate(BaseModel):
    """
    Schema for updating an existing text block. All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(None, description="Updated label for the text block.")
    tag_ids: Optional[List[int]] = Field(
        None, description="Updated list of associated tag IDs."
    )


class TextblockRead(TextblockBase):
    """
    Read schema for a text block, including metadata fields and associated tags.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the text block.")
    tags: Optional[List["TagRead"]] = Field(
        default_factory=list, description="List of associated tags."
    )
    gemeinde_id: int = Field(..., description="ID of the associated municipality.")
    gemeinde: "GemeindeRead" = Field(
        ..., description="Detailed information about the associated municipality."
    )
    autor: Optional["UserRead"] = Field(
        None, description="User who created the text block."
    )
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the text block."
    )


# Late imports for forward references
from app.schemas.tag import TagRead
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user import UserRead
