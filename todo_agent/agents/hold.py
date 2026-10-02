from datetime import datetime, timezone
from todo_agent.models import Task, TaskFinding

def inspect_task(task: Task):
    if "hold" not in task.bucket.lower():
        return []
    out=[]
    text=(task.description or "").lower()
    required={
      "hold_reason": ("reason","hold reason"),
      "resume_condition": ("resume","resume condition"),
      "review_date": ("review date","review:")
    }
    for kind, needles in required.items():
        if not any(x in text for x in needles):
            out.append(TaskFinding(task.id,task.title,kind,1,f"HOLD task missing {kind}"))
    return out
