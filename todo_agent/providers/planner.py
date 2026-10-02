import json, subprocess
from todo_agent.models import Task
from todo_agent.providers.base import TaskProvider

class PlannerProvider(TaskProvider):
    def __init__(self, plan_id: str):
        self.plan_id = plan_id

    def provider_name(self) -> str:
        return "microsoft_planner"

    def _graph(self, url: str):
        cmd = ["az.cmd","rest","--method","get","--url",url,"--output","json"]
        raw = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
        return json.loads(raw)

    def list_tasks(self) -> list[Task]:
        buckets = self._graph(
            f"https://graph.microsoft.com/v1.0/planner/plans/{self.plan_id}/buckets"
        )["value"]
        tasks = self._graph(
            f"https://graph.microsoft.com/v1.0/planner/plans/{self.plan_id}/tasks"
        )["value"]
        bucket_map = {b["id"]: b["name"].strip() for b in buckets}
        out = []
        for raw in tasks:
            try:
                detail = self._graph(
                    f"https://graph.microsoft.com/v1.0/planner/tasks/{raw['id']}/details"
                )
            except Exception:
                detail = {"description":"","checklist":{}}
            out.append(Task(
                id=raw["id"],
                title=raw.get("title",""),
                bucket=bucket_map.get(raw.get("bucketId"),""),
                due=raw.get("dueDateTime"),
                created=raw.get("createdDateTime"),
                percent_complete=raw.get("percentComplete",0),
                priority=raw.get("priority",5),
                description=detail.get("description",""),
                assignments=raw.get("assignments",{}),
                checklist=detail.get("checklist",{}),
                raw=raw,
            ))
        return out
