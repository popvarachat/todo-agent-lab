import json, subprocess
from todo_agent.models import Task
from todo_agent.providers.base import TaskProvider

class MicrosoftToDoProvider(TaskProvider):
    def __init__(self, list_id: str = "all"):
        self.list_id = list_id

    def provider_name(self) -> str:
        return "microsoft_todo"

    def _graph(self, url: str):
        cmd=["az.cmd","rest","--method","get","--url",url,"--output","json"]
        raw=subprocess.check_output(cmd,text=True,encoding="utf-8",errors="replace")
        return json.loads(raw)

    def _lists(self):
        return self._graph("https://graph.microsoft.com/v1.0/me/todo/lists")["value"]

    def list_tasks(self) -> list[Task]:
        lists=self._lists()
        if self.list_id != "all":
            lists=[x for x in lists if x["id"] == self.list_id]
        out=[]
        for lst in lists:
            url=f"https://graph.microsoft.com/v1.0/me/todo/lists/{lst['id']}/tasks"
            for raw in self._graph(url).get("value",[]):
                status=raw.get("status","notStarted")
                completed=100 if status=="completed" else 50 if status=="inProgress" else 0
                due=(raw.get("dueDateTime") or {}).get("dateTime")
                created=raw.get("createdDateTime")
                body=(raw.get("body") or {}).get("content","")
                out.append(Task(
                    id=raw["id"], title=raw.get("title",""), bucket=lst.get("displayName",""),
                    due=due, created=created, percent_complete=completed,
                    priority=1 if raw.get("importance")=="high" else 5,
                    description=body, assignments={}, checklist={}, raw=raw
                ))
        return out
