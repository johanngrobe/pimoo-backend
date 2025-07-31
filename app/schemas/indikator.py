from typing import List, Optional

from pydantic import BaseModel, computed_field, ConfigDict, Field


class IndikatorBase(BaseModel):
    """
    Base schema for an Indikator, representing a data source with a label and optional URL.
    """

    name: str = Field(..., description="The name or title of the Indikator.")
    quelle_url: Optional[str] = Field(
        None, description="The URL of the source for the Indikator data."
    )
    gemeindespezifisch: bool = Field(
        False,
        description="Gibt an, ob der Indikator mit anderen Gemeinden geteilt wird oder gemeindespezifisch ist",
    )


class IndikatorCreate(IndikatorBase):
    """
    Schema for creating a new Indikator, including optional tags by ID.
    """

    tag_ids: Optional[List[int]] = Field(
        default_factory=list,
        description="List of tag IDs associated with the Indikator.",
    )


class IndikatorUpdate(BaseModel):
    """
    Schema for updating an Indikator. All fields are optional for partial updates.
    """

    name: Optional[str] = Field(
        None, description="Updated name or title of the Indikator."
    )
    quelle_url: Optional[str] = Field(
        None, description="Updated URL of the source for the Indikator data."
    )
    gemeindespezifisch: Optional[bool] = Field(
        None,
        description="Updated status of whether the Indikator is shared with other municipalities or is municipality-specific.",
    )
    tag_ids: Optional[List[int]] = Field(
        None, description="Updated list of tag IDs associated with the Indikator."
    )


class IndikatorBaseRead(IndikatorBase):
    """
    Basic read schema for an Indikator, including metadata fields such as author and last editor.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Indikator.")
    gemeinde_id: int = Field(
        ..., description="ID of the municipality associated with this Indikator."
    )
    autor: Optional["UserRead"] = Field(
        None, description="User who created the Indikator."
    )
    letzter_bearbeiter: Optional["UserRead"] = Field(
        None, description="User who last edited the Indikator."
    )


class IndikatorRead(IndikatorBaseRead):
    """
    Detailed read schema for an Indikator, including associated tags.
    """

    tags: Optional[List["TagRead"]] = Field(
        default_factory=list, description="List of tags associated with the Indikator."
    )

    @computed_field
    @property
    def tag_ids(self) -> List[int]:
        """
        Automatically computes the list of tag IDs from the tags.
        """
        return [tag.id for tag in self.tags or []]


from app.schemas.tag import TagRead
from app.schemas.user import UserRead
