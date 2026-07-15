from typing import Optional

from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):
    title: str
    description: Optional[str] = None

# При создании мы обязаны указать, какому юзеру принадлежит процесс
class WorkflowCreate(WorkflowBase):
    user_id: int 

# В ответе мы возвращаем все поля, включая присвоенный базой ID и статус
class WorkflowResponse(WorkflowBase):
    id: int
    status: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class WorkflowUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None