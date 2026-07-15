from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.models.user import User
from src.db.models.workflow import Workflow
from src.db.models.workflow_step import WorkflowStep
from src.db.session import get_db
from src.dependencies import (
    get_execution_engine,
    get_workflow_run_service,
    get_workflow_step_service,
)
from src.engine.execution_engine import ExecutionEngine, UnsafeUrlError
from src.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate
from src.schemas.workflow_step import WorkflowStepCreate, WorkflowStepResponse
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_step_service import WorkflowStepService

router = APIRouter()

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow_in: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1. Сначала проверяем, существует ли вообще такой пользователь
    # Мы используем db.get, так как ищем по Primary Key (ID)
    user = await db.get(User, workflow_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Создаем задачу
    new_workflow = Workflow(
        title=workflow_in.title,
        description=workflow_in.description,
        user_id=workflow_in.user_id
    )
    db.add(new_workflow)
    await db.commit()
    await db.refresh(new_workflow)
    
    return new_workflow

@router.get("/user/{user_id}", response_model=list[WorkflowResponse])
async def get_user_workflows(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получить все рабочие процессы конкретного пользователя
    """
    # Вытаскиваем все записи, где user_id совпадает с запрошенным
    query = select(Workflow).where(Workflow.user_id == user_id)
    result = await db.execute(query)
    workflows = result.scalars().all()
    
    return workflows

@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: int,
    execution_engine: ExecutionEngine = Depends(get_execution_engine),
):
    """
    Запустить рабочий процесс через ExecutionEngine
    """
    try:
        workflow_run = await execution_engine.execute_workflow(workflow_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Workflow not found")
    except UnsafeUrlError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "run_id": workflow_run.id,
        "status": workflow_run.status,
        "result": workflow_run.result,
    }

@router.get("/{workflow_id}/runs")
async def get_workflow_runs(
    workflow_id: int,
    workflow_run_service: WorkflowRunService = Depends(get_workflow_run_service),
):
    """
    Получить историю всех запусков рабочего процесса
    """
    runs = await workflow_run_service.list_workflow_runs_by_workflow(workflow_id)

    return [
        {
            "id": run.id,
            "status": run.status,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
            "result": run.result,
            "error": run.error,
        }
        for run in runs
    ]

@router.post("/{workflow_id}/steps", response_model=WorkflowStepResponse)
async def create_workflow_step(
    workflow_id: int,
    step_in: WorkflowStepCreate,
    db: AsyncSession = Depends(get_db),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
):
    """
    Создать шаг рабочего процесса
    """
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    new_step = WorkflowStep(
        workflow_id=workflow_id,
        title=step_in.title,
        prompt=step_in.prompt,
        step_order=step_in.step_order,
        step_type=step_in.step_type,
    )
    return await workflow_step_service.create_step(new_step)

@router.get("/{workflow_id}/steps", response_model=list[WorkflowStepResponse])
async def get_workflow_steps(
    workflow_id: int,
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
):
    """
    Получить все шаги рабочего процесса в порядке step_order
    """
    return await workflow_step_service.list_workflow_steps(workflow_id)

@router.patch("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int, 
    workflow_in: WorkflowUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить существующий рабочий процесс (например, изменить статус)
    """
    # 1. Ищем задачу в базе
    workflow = await db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # 2. Получаем только те поля, которые клиент реально прислал для обновления
    update_data = workflow_in.model_dump(exclude_unset=True)
    
    # 3. Применяем новые значения к объекту базы данных
    for field, value in update_data.items():
        setattr(workflow, field, value)
        
    # 4. Сохраняем изменения
    await db.commit()
    await db.refresh(workflow)
    
    return workflow