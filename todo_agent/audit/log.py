import json
from pathlib import Path
from datetime import datetime, timezone

def append_event(path: Path, event: str, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    row={"ts":datetime.now(timezone.utc).isoformat(),"event":event,"data":data}
    with path.open("a",encoding="utf-8") as f:
        f.write(json.dumps(row,ensure_ascii=False)+"\n")
