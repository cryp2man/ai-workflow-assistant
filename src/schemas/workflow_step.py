from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

StepType = Literal["llm", "http"]


class WorkflowStepBase(BaseModel):
    title: str
    prompt: str
    step_order: int
    step_type: StepType = "llm"

# workflow_id не принимаем в body: он приходит из Path
class WorkflowStepCreate(WorkflowStepBase):
    pass

# В ответе возвращаем все поля, включая присвоенный базой ID
class WorkflowStepResponse(WorkflowStepBase):
    id: int
    workflow_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WorkflowStepUpdate(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    step_order: Optional[int] = None
    step_type: Optional[StepType] = None
