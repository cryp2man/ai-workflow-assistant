from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.db.models.workflow import Workflow


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[int] = mapped_column(
        ForeignKey("workflows.id"),
        nullable=False,
        index=True,
    )
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # Тип шага: "llm" — prompt уходит в LLM, "http" — prompt содержит URL
    step_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="llm",
        server_default="llm",
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Пока односторонняя связь: back_populates="steps" требует парного свойства
    # Workflow.steps, а менять Workflow запрещено. Обе стороны свяжет отдельная
    # задача, которая добавит steps в Workflow.
    workflow: Mapped["Workflow"] = relationship()
