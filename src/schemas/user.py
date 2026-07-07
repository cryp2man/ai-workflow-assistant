from pydantic import BaseModel, EmailStr, ConfigDict

# Базовая схема
class UserBase(BaseModel):
    username: str
    email: EmailStr  # Pydantic сам проверит наличие @ и домена

# Схема для создания пользователя (то, что мы получаем от клиента)
class UserCreate(UserBase):
    pass

# Схема ответа (то, что мы отправляем обратно клиенту)
class UserResponse(UserBase):
    id: int
    
    # Разрешаем Pydantic читать данные напрямую из объектов SQLAlchemy
    model_config = ConfigDict(from_attributes=True)