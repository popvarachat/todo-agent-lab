from todo_agent.models import Task, TaskFinding

def inspect_task(task: Task):
    out=[]
    if not task.assignments:
        out.append(TaskFinding(task.id,task.title,"no_owner",1,"ไม่มี Owner"))
    if not task.due:
        out.append(TaskFinding(task.id,task.title,"no_due",1,"ไม่มี Due date"))
    if not task.description.strip():
        out.append(TaskFinding(task.id,task.title,"no_description",1,"ไม่มี Description"))
    if not task.checklist:
        out.append(TaskFinding(task.id,task.title,"no_checklist",1,"ไม่มี Checklist"))
    return out
