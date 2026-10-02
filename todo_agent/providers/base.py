from abc import ABC, abstractmethod
from todo_agent.models import Task

class TaskProvider(ABC):
    @abstractmethod
    def list_tasks(self) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError
