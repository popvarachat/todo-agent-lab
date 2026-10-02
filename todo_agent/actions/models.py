from dataclasses import dataclass, field
from typing import Any

@dataclass
class ActionProposal:
    id: str
    task_id: str
    title: str
    action_type: str
    reason: str
    risk: str = "low"
    payload: dict[str, Any] = field(default_factory=dict)
    status: str = "proposed"
