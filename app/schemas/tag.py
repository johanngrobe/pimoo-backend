from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TagBase(BaseModel):
    """
    Base schema for a tag, containing the label.
    """

    name: str = Field(..., description="Name des Tags")
    gemeindespezifisch: bool = Field(
        False,
        description="Gibt an, ob der Tag mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )


class TagCreate(TagBase):
    """
    Schema for creating a new tag. Inherits fields from TagBase.
    """

    pass


class TagUpdate(BaseModel):
    """
    Schema for updating an existing tag, allowing partial updates.
    """

    name: Optional[str] = Field(None, description="Neue Name des Tags")
    gemeindespezifisch: Optional[bool] = Field(
        None, description="Neuer Status der Gemeindespezifität des Tags"
    )


class TagRead(TagBase):
    """
    Read schema for a tag, including metadata fields such as ID, municipality, author, and last editor.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the tag.")
    gemeinde_id: int = Field(
        ..., description="ID of the municipality associated with this tag."
    )
    gemeinde: "GemeindeRead" = Field(
        ..., description="Details of the associated municipality."
    )
    autor: Optional["UserRead"] = Field(None, description="User who created the tag.")
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the tag."
    )


# Late imports for forward references
from app.schemas.gemeinde import GemeindeRead
from app.schemas.user import UserRead
