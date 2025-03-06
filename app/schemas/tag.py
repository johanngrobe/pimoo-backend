from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TagBase(BaseModel):
    """
    Base schema for a tag, containing the label.
    """

    label: str = Field(..., description="The descriptive label for the tag.")


class TagCreate(TagBase):
    """
    Schema for creating a new tag. Inherits fields from TagBase.
    """

    pass


class TagUpdate(BaseModel):
    """
    Schema for updating an existing tag, allowing partial updates.
    """

    label: Optional[str] = Field(None, description="Updated label for the tag.")


class TagRead(TagBase):
    """
    Read schema for a tag, including metadata fields such as ID, municipality, author, and last editor.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the tag.")
    municipality_id: int = Field(
        ..., description="ID of the municipality associated with this tag."
    )
    municipality: "MunicipalityRead" = Field(
        ..., description="Details of the associated municipality."
    )
    author: Optional["UserRead"] = Field(None, description="User who created the tag.")
    last_editor: Optional["UserRead"] = Field(
        None, description="User who last edited the tag."
    )


# Late imports for forward references
from app.schemas.municipality import MunicipalityRead
from app.schemas.user import UserRead
