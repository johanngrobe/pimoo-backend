from uuid import UUID
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from fastapi_mail import MessageSchema, MessageType
from .fastmail import Mail

from ..database import get_user_db
from .. import models
from ..config import settings


class UserManager(UUIDIDMixin, BaseUserManager[models.User, UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: models.User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

        user_dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "municipality": user.municipality.name,
        }
        print(user_dict)

        message = MessageSchema(
        subject="Willkommen beim Mobilitätscheck für Magistratsvorlagen von pimoo",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html
        )
        try:
            await Mail.send_message(message, template_name="welcome-user.html")
        except:
            print("Error sending welcome email")

    async def on_after_forgot_password(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

        user_dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "token": token
        }
        print(user)

        message = MessageSchema(
        subject="Passwort zurücksetzen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html
        )

        await Mail.send_message(message, template_name="reset-password.html")

    async def on_after_request_verify(
        self, user: models.User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

        user_dict = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "municipality": user.municipality.name,
            "token": token
        }

        message = MessageSchema(
        subject="Willkommen beim Mobilitätscheck für Magistratsvorlagen von pimoo",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html
        )

        await Mail.send_message(message, template_name="confirm-account.html")
        

    async def on_after_verify(
        self, user: models.User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(cookie_httponly=True, cookie_secure=True, cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET_KEY, lifetime_seconds=settings.JWT_LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[models.User, UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)