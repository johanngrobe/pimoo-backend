from fastapi_mail import MessageSchema, MessageType

from app.config import settings
from app.models import User
from app.services.mail.config_mail import Mail
from app.utils.options_util import USER_ROLES
from app.utils.url_util import add_query_params


async def send_welcome(user: User):

    user_dict = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": USER_ROLES[user.role],
        "municipality": user.municipality.name,
    }

    message = MessageSchema(
        subject="Willkommen beim Mobilitätscheck für Magistratsvorlagen von pimoo",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )
    try:
        await Mail.send_message(message, template_name="welcome-user.html")
    except:
        print("Error sending welcome email")


async def send_verification(user: User, token: str):
    url = add_query_params(
        f"{settings.VITE_FRONTEND_URL}/verify-account", {"token": token}
    )

    user_dict = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": USER_ROLES[user.role],
        "municipality": user.municipality.name,
        "url": url,
    }

    message = MessageSchema(
        subject="Account bestätigen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )

    await Mail.send_message(message, template_name="verify-account.html")


async def send_reset_password(user: User, token: str):

    url = add_query_params(
        f"{settings.VITE_FRONTEND_URL}/reset-password", {"token": token}
    )

    user_dict = {"first_name": user.first_name, "last_name": user.last_name, "url": url}

    message = MessageSchema(
        subject="Passwort zurücksetzen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )

    await Mail.send_message(message, template_name="reset-password.html")
