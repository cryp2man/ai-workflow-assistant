from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models.user import User
from src.schemas.user import UserCreate, UserResponse

# Импорт функции для получения сессии базы данных
# (Убедись, что путь к get_db совпадает с твоей структурой проекта)
from src.db.session import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Проверяем, нет ли уже пользователя с таким email
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    db_user = result.scalars().first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Создаем нового пользователя
    new_user = User(username=user_in.username, email=user_in.email)
    db.add(new_user)
    
    # 3. Сохраняем в базу и обновляем объект
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

# Добавь эти эндпоинты в конец файла src/api/v1/users.py

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Получить список всех пользователей с пагинацией
    """
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить конкретного пользователя по ID
    """
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalars().first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user