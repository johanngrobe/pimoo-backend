from __future__ import annotations

from app.crud.exceptions import AuthorizationError


def check_user_authorization(user: User, gemeinde_id: int):
    """
    Check if a user is authorized to access a specific municipality.

    :param user: The user instance to check.
    :param municipality_id: The ID of the municipality to access.
    :raises AuthorizationError: If the user is not authorized to access the resource.
    """
    grant_access = True

    if not (gemeinde_id == user.gemeinde_id):
        grant_access = False

    if user.is_superuser:
        grant_access = True

    if not grant_access:
        raise AuthorizationError(
            detail="User is not authorized to access this resource"
        )
