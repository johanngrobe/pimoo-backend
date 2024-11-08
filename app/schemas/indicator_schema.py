from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IndicatorBase(BaseModel):
    """
    Base schema for an indicator, representing a data source with a label and optional URL.
    """

    label: str = Field(..., description="The name or title of the indicator.")
    source_url: Optional[str] = Field(
        None, description="The URL of the source for the indicator data."
    )


class IndicatorCreate(IndicatorBase):
    """
    Schema for creating a new indicator, including optional tags by ID.
    """

    tag_ids: Optional[List[int]] = Field(
        default_factory=list,
        description="List of tag IDs associated with the indicator.",
    )


class IndicatorID(BaseModel):
    """
    Schema for an indicator reference by ID, used for linking or simple associations.
    """

    id: int = Field(..., description="Unique identifier for the indicator.")


class IndicatorUpdate(BaseModel):
    """
    Schema for updating an indicator. All fields are optional for partial updates.
    """

    label: Optional[str] = Field(
        None, description="Updated name or title of the indicator."
    )
    source_url: Optional[str] = Field(
        None, description="Updated URL of the source for the indicator data."
    )
    tag_ids: Optional[List[int]] = Field(
        None, description="Updated list of tag IDs associated with the indicator."
    )


class IndicatorBasicRead(IndicatorBase):
    """
    Basic read schema for an indicator, including metadata fields such as author and last editor.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the indicator.")
    municipality_id: int = Field(
        ..., description="ID of the municipality associated with this indicator."
    )
    author: Optional["UserRead"] = Field(
        None, description="User who created the indicator."
    )
    last_editor: Optional["UserRead"] = Field(
        None, description="User who last edited the indicator."
    )


class IndicatorDetailRead(IndicatorBasicRead):
    """
    Detailed read schema for an indicator, including associated tags.
    """

    tags: Optional[List["TagRead"]] = Field(
        default_factory=list, description="List of tags associated with the indicator."
    )


from app.schemas.tag_schema import TagRead
from app.schemas.user_schema import UserRead
