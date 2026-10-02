from dataclasses import dataclass, field
from typing import Any

@dataclass
class Task:
    id: str
    title: str
    bucket: str = ""
    due: str | None = None
    created: str | None = None
    percent_complete: int = 0
    priority: int = 5
    description: str = ""
    assignments: dict[str, Any] = field(default_factory=dict)
    checklist: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

@dataclass
class TaskFinding:
    task_id: str
    title: str
    kind: str
    severity: int
    message: str
