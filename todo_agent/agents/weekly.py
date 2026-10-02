from collections import Counter
from todo_agent.models import TaskFinding

def build_weekly_summary(active_count: int, findings: list[TaskFinding]) -> dict:
    counts=Counter(f.kind for f in findings)
    return {
        "active": active_count,
        "overdue": counts.get("overdue",0),
        "stale": counts.get("stale",0),
        "due_soon": counts.get("due_soon",0),
        "urgent": counts.get("urgent",0),
        "quality_issues": sum(counts.get(k,0) for k in (
            "no_owner","no_due","no_description","no_checklist"
        ))
    }
