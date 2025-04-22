from app.core.db import Base

from app.models.association_indicator_tag import indicator_tag_association
from app.models.association_results_indicators import (
    mobility_results_indicators_association,
)
from app.models.association_text_block_tag import text_block_tag_association
from app.models.climate_submission import ClimateSubmission
from app.models.indicator import Indicator
from app.models.main_objective import MainObjective
from app.models.mobility_result import MobilityResult
from app.models.mobility_submission import MobilitySubmission
from app.models.mobility_subresult import MobilitySubresult
from app.models.municipality import Municipality
from app.models.sub_objective import SubObjective
from app.models.tag import Tag
from app.models.text_block import TextBlock
from app.models.user import User
