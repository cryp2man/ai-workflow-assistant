from src.repositories.workflow_repository import WorkflowRepository


class WorkflowService:
    """Сервис рабочих процессов. Пока только конструктор.

    Бизнес-логика, CRUD, работа с БД здесь намеренно не реализованы.
    """

    def __init__(self, repository: WorkflowRepository) -> None:
        self.repository = repository
