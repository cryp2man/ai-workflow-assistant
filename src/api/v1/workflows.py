from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.session import get_db
from src.db.models.workflow import Workflow
from src.db.models.user import User
from src.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate

router = APIRouter()

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(workflow_in: WorkflowCreate, db: AsyncSession = Depends(get_db)):
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