from todo_agent.models import Task, TaskFinding

def suggest(task: Task, findings: list[TaskFinding]) -> list[str]:
    kinds={f.kind for f in findings}
    out=[]
    if "overdue" in kinds:
        out.append("Follow up owner and confirm a new due date")
    if "stale" in kinds:
        out.append("Request a meaningful status update")
    if "no_owner" in kinds:
        out.append("Assign an accountable owner")
    if "no_due" in kinds:
        out.append("Set a realistic due date")
    if "no_description" in kinds:
        out.append("Add outcome / definition of done")
    if "no_checklist" in kinds:
        out.append("Add at least one measurable next step")
    if "hold" in task.bucket.lower():
        out.append("Review hold reason, resume condition and review date")
    return out
