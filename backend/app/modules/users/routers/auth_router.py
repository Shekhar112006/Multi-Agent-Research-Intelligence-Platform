from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.schemas.token import Token
from app.modules.users.schemas.user_login import UserLogin
from app.core.security.dependencies import get_current_user
from app.modules.users.models.users import User
from app.core.security.dependencies import get_current_user
from app.modules.users.models.users import User

from app.core.database import get_db
from app.modules.users.schemas.user_create import UserCreate
from app.modules.users.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    user = service.register(user_data)

    return {
        "message": "User registered successfully.",
        "user_id": str(user.id),
    }

@router.post(
    "/login",
    response_model=Token,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.login(user_data)


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
    }