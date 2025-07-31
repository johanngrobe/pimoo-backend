from fastapi_mail import MessageSchema, MessageType

from app.core.config import settings
from app.models.user import User
from app.services.mail.config_mail import Mail
from app.utils.url_util import add_query_params


async def send_welcome(user: User):

    user_dict = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "gemeinde": user.gemeinde.name,
    }

    message = MessageSchema(
        subject="Willkommen beim Mobilitätscheck für Magistratsvorlagen von pimoo",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )
    try:
        await Mail.send_message(message, template_name="account-registrieren.html")
    except:
        print("Error sending welcome email")


async def send_verification(user: User, token: str):
    url = add_query_params(
        f"{settings.FRONTEND_HOST}/auth/account-bestaetigen", {"token": token}
    )

    user_dict = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "gemeinde": user.gemeinde.name,
        "url": url,
    }

    message = MessageSchema(
        subject="Account bestätigen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )

    await Mail.send_message(message, template_name="account-bestaetigen.html")


async def send_reset_password(user: User, token: str):

    url = add_query_params(
        f"{settings.FRONTEND_HOST}/auth/passwort-zuruecksetzen", {"token": token}
    )

    user_dict = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "url": url,
    }

    message = MessageSchema(
        subject="Passwort zurücksetzen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )

    await Mail.send_message(message, template_name="passwort-zuruecksetzen.html")
