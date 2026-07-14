from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.db.models.user import User
from src.dependencies import get_user_service
from src.schemas.user import UserCreate, UserResponse
from src.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
):
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        telegram_id=user_in.telegram_id,
    )
    try:
        return await service.create_user(new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.get("/", response_model=list[UserResponse])
async def read_users(service: UserService = Depends(get_user_service)):
    """
    Получить список всех пользователей
    """
    return await service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Получить конкретного пользователя по ID
    """
    db_user = await service.get_user(user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
