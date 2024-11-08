from app.crud.exceptions import AuthorizationError
from app.models import User


def check_user_authorization(user: User, municipality_id: int):
    grant_access = True

    if not (municipality_id == user.municipality_id):
        grant_access = False

    if user.is_superuser:
        grant_access = True

    if not grant_access:
        raise AuthorizationError(
            detail="User is not authorized to access this resource"
        )
