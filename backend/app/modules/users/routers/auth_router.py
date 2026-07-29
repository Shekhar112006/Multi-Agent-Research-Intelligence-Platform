from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.modules.users.schemas.token import Token
from app.modules.users.schemas.user_login import UserLogin

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