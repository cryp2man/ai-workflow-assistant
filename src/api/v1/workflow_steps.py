from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.dependencies import get_workflow_step_service
from src.schemas.workflow_step import WorkflowStepResponse, WorkflowStepUpdate
from src.services.workflow_step_service import WorkflowStepService

router = APIRouter()

@router.get("/{step_id}", response_model=WorkflowStepResponse)
async def get_workflow_step(
    step_id: int,
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
):
    """
    Получить один шаг рабочего процесса по ID
    """
    step = await workflow_step_service.get_step(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Workflow step not found")

    return step

@router.patch("/{step_id}", response_model=WorkflowStepResponse)
async def update_workflow_step(
    step_id: int,
    step_in: WorkflowStepUpdate,
    db: AsyncSession = Depends(get_db),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
):
    """
    Частично обновить шаг рабочего процесса
    """
    step = await workflow_step_service.get_step(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Workflow step not found")

    # Получаем только те поля, которые клиент реально прислал для обновления
    update_data = step_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(step, field, value)

    await db.commit()
    await db.refresh(step)

    return step

@router.delete("/{step_id}", status_code=204)
async def delete_workflow_step(
    step_id: int,
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
):
    """
    Удалить шаг рабочего процесса
    """
    step = await workflow_step_service.get_step(step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Workflow step not found")

    await workflow_step_service.delete_step(step)
