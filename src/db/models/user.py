# Полное содержимое файла src/db/models/user.py

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    # Telegram user ID: BigInteger, т.к. значения превышают диапазон INT32.
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    # Связь с таблицей workflows
    workflows: Mapped[list["Workflow"]] = relationship(back_populates="user", cascade="all, delete-orphan")