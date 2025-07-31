from typing import List, Optional

from pydantic import BaseModel, Field, computed_field, ConfigDict


class TextblockBase(BaseModel):
    """
    Base schema for a text block, containing a label.
    """

    name: str = Field(..., description="The label or title for the text block.")
    gemeindespezifisch: bool = Field(
        False,
        description="Gibt an, ob der Textblock mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )


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
    gemeindespezifisch: Optional[bool] = Field(
        False,
        description="Gibt an, ob der Tag mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )
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

    @computed_field
    @property
    def tag_ids(self) -> List[int]:
        """
        Automatically computes the list of tag IDs from the tags.
        """
        return [tag.id for tag in self.tags or []]


# Late imports for forward references
from app.schemas.tag import TagRead
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user import UserRead
