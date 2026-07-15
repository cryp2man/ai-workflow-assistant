from datetime import datetime

from src.db.models.workflow_run import WorkflowRun
from src.llm.base import BaseLLMProvider
from src.prompts.builder import PromptBuilder
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService


class ExecutionEngine:
    """Движок выполнения Workflow.

    Первая итерация: фиксирует факт запуска (WorkflowRun со статусом
    "running"). Завершение, ошибки и LLM-шаги — в следующих задачах.
    """

    def __init__(
        self,
        workflow_service: WorkflowService,
        workflow_run_service: WorkflowRunService,
        prompt_builder: PromptBuilder,
        llm_provider: BaseLLMProvider,
    ) -> None:
        self.workflow_service = workflow_service
        self.workflow_run_service = workflow_run_service
        self.prompt_builder = prompt_builder
        self.llm_provider = llm_provider

    async def execute_workflow(
        self,
        workflow_id: int,
    ) -> WorkflowRun:
        """Запустить workflow: создать WorkflowRun и довести его до completed."""
        workflow = await self.workflow_service.get_workflow(workflow_id)
        if workflow is None:
            raise ValueError("Workflow not found")

        prompt = self.prompt_builder.build_prompt(
            getattr(workflow, "title", "Execute workflow")
        )
        response = await self.llm_provider.generate(prompt)

        workflow_run = WorkflowRun(
            workflow_id=workflow.id,
            status="running",
            started_at=datetime.utcnow(),
            finished_at=None,
            result=None,
            error=None,
        )
        workflow_run = await self.workflow_run_service.create_workflow_run(
            workflow_run
        )

        workflow_run.status = "completed"
        workflow_run.finished_at = datetime.utcnow()
        workflow_run.result = {"response": response}
        await self.workflow_run_service.repository.session.commit()

        return workflow_run
