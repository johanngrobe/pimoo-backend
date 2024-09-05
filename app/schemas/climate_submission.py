from pydantic import BaseModel, field_serializer, ConfigDict
from typing import Optional
from datetime import datetime, date
from ..utils.label import label_climate_impact, label_climate_impact_ghg, label_climate_impact_duration

class ClimateSubmissionBase(BaseModel):
    author: str
    administration_no: str
    administration_date: date
    label: str
    impact: str
    impact_ghg: Optional[int] = None
    impact_adaption: Optional[int] = None
    impact_desc: Optional[str] = None
    impact_duration: Optional[str] = None
    alternative_desc: Optional[str] = None

class ClimateSubmissionCreate(ClimateSubmissionBase):
    pass

class ClimateSubmissionOut(ClimateSubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime

    # Define the fields for translated labels
    impact_label: Optional[str] = None
    impact_ghg_label: Optional[str] = None
    impact_adaption_label: Optional[str] = None
    impact_duration_label: Optional[str] = None

    # Add computed labels using field_serializer
    @field_serializer("impact_label", when_used="json")
    def add_climate_impact_label(self, _):
        return label_climate_impact(self.impact)

    @field_serializer("impact_ghg_label", when_used="json")
    def add_climate_impact_ghg_label(self, _):
        return label_climate_impact_ghg(self.impact_ghg)

    @field_serializer("impact_adaption_label", when_used="json")
    def add_climate_impact_adaption_label(self, _):
        return label_climate_impact_ghg(self.impact_adaption)

    @field_serializer("impact_duration_label", when_used="json")
    def add_climate_impact_duration_label(self, _):
        return label_climate_impact_duration(self.impact_duration)
