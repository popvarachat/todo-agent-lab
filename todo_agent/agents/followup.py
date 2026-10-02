from todo_agent.models import Task, TaskFinding

def build_message(task: Task, findings: list[TaskFinding]) -> str | None:
    kinds={f.kind for f in findings}
    if not ({"overdue","stale"} & kinds):
        return None
    reasons=[]
    if "overdue" in kinds: reasons.append("เลยกำหนด")
    if "stale" in kinds: reasons.append("ไม่มีความคืบหน้าตามเกณฑ์")
    reason=" และ ".join(reasons)
    return (
      f"ขอติดตามงาน: {task.title}\n"
      f"สถานะระบบพบว่า {reason}. "
      "รบกวนอัปเดตสถานะล่าสุด, blocker (ถ้ามี), และกำหนดการถัดไปครับ"
    )
