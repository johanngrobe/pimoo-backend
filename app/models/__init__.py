# Association Models
from app.models.association_indicator_tag_model import indicator_tag_association
from app.models.association_text_block_tag_model import text_block_tag_association
from app.models.association_results_indicators_model import (
    mobility_results_indicators_association,
)

# Models
from app.models.user_model import User
from app.models.municipality_model import Municipality
from app.models.main_objective_model import MainObjective
from app.models.sub_objective_model import SubObjective
from app.models.tag_model import Tag
from app.models.text_block_model import TextBlock
from app.models.indicator_model import Indicator
from app.models.mobility_submission_model import MobilitySubmission
from app.models.mobility_result_model import MobilityResult
from app.models.mobility_subresult_model import MobilitySubresult
from app.models.climate_submission_model import ClimateSubmission
