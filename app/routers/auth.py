from fastapi import Response, Depends, APIRouter
from ..utils.fastapi_users import current_active_user
from fastapi_users.authentication import JWTStrategy
from ..utils.fastapi_users import get_jwt_strategy, current_active_user, auth_backend


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

# @router.post("/jwt/refresh")
# async def refresh_jwt(response: Response, jwt_strategy: JWTStrategy = Depends(get_jwt_strategy), user=Depends(current_active_user)):
#     return await auth_backend.login(jwt_strategy, user)
