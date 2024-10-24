from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from ...config import settings
from ... import schemas
from pathlib import Path


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME= settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = settings.USE_CREDENTIALS,
    VALIDATE_CERTS = settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)

# Usage
Mail = FastMail(conf)

# async def send_user_confirmation(user: schemas.UserOut, subject: str = 'Account bestätigen'):

#     user_dict = user.model_dump()
#     user_dict["confirmation_link"] = f"{settings.CONFIRMATION_URL}{user.id}"

#     message = MessageSchema(
#         subject=subject,
#         recipients=[user.email],  # List of recipients
#         template_body=user_dict,
#         subtype=MessageType.html
#     )

#     await Mail.send_message(message, template_name="confirm-user.html")


    
# async def send_reset_password(user: dict, subject: str = 'Passwort zurücksetzen'):

#     user_dict = user
#     user["confirmation_link"] = f"{settings.CONFIRMATION_URL}{user_dict.id}"


#     message = MessageSchema(
#         subject=subject,
#         recipients=[user_dict.email],  # List of recipients
#         template_body=user_dict,
#         subtype=MessageType.html
#     )

#     await Mail.send_message(message, template_name="reset-password.html")

