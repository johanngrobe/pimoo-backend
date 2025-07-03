from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GemeindeBase(BaseModel):
    """
    Base schema for a Gemeinde, containing the primary name attribute.
    """

    name: str = Field(..., description="The name of the Gemeinde.")


class GemeindeCreate(GemeindeBase):
    """
    Schema for creating a new Gemeinde. Inherits fields from GemeindeBase.
    """

    pass


class GemeindeUpdate(BaseModel):
    """
    Schema for updating an existing Gemeinde. Allows partial updates.
    """

    name: Optional[str] = Field(None, description="The updated name of the Gemeinde.")


class GemeindeRead(GemeindeBase):
    """
    Read schema for a Gemeinde, including the unique identifier.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Gemeinde.")
