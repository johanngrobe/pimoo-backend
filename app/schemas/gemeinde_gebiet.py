from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GemeindeGebietBase(BaseModel):

    name: str = Field(..., description="The name of the Gemeinde.")
    gemeinde_id: int = Field(..., description="ID of the associated Gemeinde.")


class GemeindeGebietCreate(GemeindeGebietBase):
    """
    Schema for creating a new Gemeinde. Inherits fields from GemeindeBase.
    """

    pass


class GemeindeGebietUpdate(BaseModel):
    """
    Schema for updating an existing Gemeinde. Allows partial updates.
    """

    name: Optional[str] = Field(None, description="The updated name of the Gemeinde.")


class GemeindeGebietRead(GemeindeGebietBase):
    """
    Read schema for a Gemeinde, including the unique identifier.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Gemeinde.")
    gemeinde: Optional["GemeindeRead"] = Field(
        None, description="Associated Gemeinde object."
    )


from app.schemas.gemeinde import GemeindeRead
