from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending") # pending, in_progress, completed
    
    # Внешний ключ (Foreign Key) - хранит ID владельца из таблицы users
    # ondelete="CASCADE" означает, что если удалить пользователя, все его процессы тоже удалятся
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    # Виртуальная связь для удобной работы в Python (алхимия сама подтянет объект пользователя)
    user: Mapped["User"] = relationship(back_populates="workflows")