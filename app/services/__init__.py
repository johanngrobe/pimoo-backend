from app.services.user.user_manager import UserManager
from app.services.mail.messages import (
    send_welcome,
    send_reset_password,
    send_verification,
)

from app.services.pdf.climate_submission_pdf import ClimateSubmissionPDF
from app.services.pdf.mobility_submission_pdf import MobilitySubmissionPDF
