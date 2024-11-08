from app.database import Base

# Association Models
from .association_indicator_tag_model import indicator_tag_association
from .association_text_block_tag_model import text_block_tag_association
from .association_results_indicators_model import (
    mobility_results_indicators_association,
)

# Models
from .user_model import User
from .municipality_model import Municipality
from .main_objective_model import MainObjective
from .sub_objective_model import SubObjective
from .tag_model import Tag
from .text_block_model import TextBlock
from .indicator_model import Indicator
from .mobility_submission_model import MobilitySubmission
from .mobility_result_model import MobilityResult
from .mobility_subresult_model import MobilitySubresult
from .climate_submission_model import ClimateSubmission
