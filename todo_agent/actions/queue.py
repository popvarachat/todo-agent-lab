import json, uuid
from pathlib import Path
from todo_agent.actions.models import ActionProposal

def proposal_id():
    return uuid.uuid4().hex[:12]

def save_queue(path: Path, proposals: list[ActionProposal]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([p.__dict__ for p in proposals],ensure_ascii=False,indent=2),encoding="utf-8")

def load_queue(path: Path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8-sig"))

def update_status(path: Path, proposal_id_value: str, status: str):
    rows=load_queue(path)
    found=False
    for r in rows:
        if r["id"]==proposal_id_value:
            r["status"]=status
            found=True
            break
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    return found
