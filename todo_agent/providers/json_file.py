import json
from pathlib import Path
from todo_agent.models import Task
from todo_agent.providers.base import TaskProvider

class JsonFileProvider(TaskProvider):
    def __init__(self, path: str):
        self.path = Path(path)

    def provider_name(self) -> str:
        return "json_file"

    def list_tasks(self) -> list[Task]:
        data=json.loads(self.path.read_text(encoding="utf-8"))
        rows=data["tasks"] if isinstance(data,dict) else data
        out=[]
        for r in rows:
            out.append(Task(
                id=str(r["id"]),
                title=r.get("title",""),
                bucket=r.get("bucket",""),
                due=r.get("due"),
                created=r.get("created"),
                percent_complete=r.get("percent_complete",0),
                priority=r.get("priority",5),
                description=r.get("description",""),
                assignments=r.get("assignments",{}),
                checklist=r.get("checklist",{}),
                raw=r,
            ))
        return out
