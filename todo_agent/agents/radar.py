from datetime import datetime, timezone, timedelta
from todo_agent.models import Task, TaskFinding

def _dt(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def last_activity(task: Task):
    dates = [_dt(task.created)]
    for item in task.checklist.values():
        dates.append(_dt(item.get("lastModifiedDateTime")))
    vals = [x for x in dates if x]
    return max(vals) if vals else None

def inspect_task(task: Task, stale_days=14, due_soon_days=7):
    now = datetime.now(timezone.utc)
    findings = []
    due = _dt(task.due)
    last = last_activity(task)
    if due and due < now:
        findings.append(TaskFinding(task.id,task.title,"overdue",4,"เลยกำหนดแล้ว"))
    elif due and due <= now + timedelta(days=due_soon_days):
        findings.append(TaskFinding(task.id,task.title,"due_soon",1,"ใกล้ถึงกำหนด"))
    if last and now-last >= timedelta(days=stale_days):
        findings.append(TaskFinding(task.id,task.title,"stale",2,f"ไม่มี activity >= {stale_days} วัน"))
    if task.priority <= 1:
        findings.append(TaskFinding(task.id,task.title,"urgent",2,"Planner priority สูง"))
    return findings
