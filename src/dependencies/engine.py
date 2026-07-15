from fastapi import Depends

from src.core.config import settings
from src.dependencies.services import (
    get_workflow_run_service,
    get_workflow_service,
    get_workflow_step_service,
)
from src.engine.execution_engine import ExecutionEngine
from src.llm.base import BaseLLMProvider
from src.llm.openai_compatible_provider import OpenAICompatibleProvider
from src.llm.openai_provider import OllamaProvider
from src.prompts.builder import PromptBuilder
from src.services.workflow_run_service import WorkflowRunService
from src.services.workflow_service import WorkflowService
from src.services.workflow_step_service import WorkflowStepService


def get_prompt_builder() -> PromptBuilder:
    """Слой формирования промптов (stateless)."""
    return PromptBuilder()


def get_llm_provider() -> BaseLLMProvider:
    """LLM-провайдер проекта, выбранный через LLM_PROVIDER в Settings."""
    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider(settings)
    return OpenAICompatibleProvider(settings)


def get_execution_engine(
    workflow_service: WorkflowService = Depends(get_workflow_service),
    workflow_run_service: WorkflowRunService = Depends(get_workflow_run_service),
    workflow_step_service: WorkflowStepService = Depends(get_workflow_step_service),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
) -> ExecutionEngine:
    """Движок выполнения workflow, собранный на зависимостях запроса."""
    return ExecutionEngine(
        workflow_service=workflow_service,
        workflow_run_service=workflow_run_service,
        workflow_step_service=workflow_step_service,
        prompt_builder=prompt_builder,
        llm_provider=llm_provider,
    )
