import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT/"config"/"settings.json").read_text(encoding="utf-8"))
PLAN = CFG["plan_id"]

def graph(url):
    cmd = ["az.cmd","rest","--method","get","--url",url,"--output","json"]
    raw = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
    return json.loads(raw)

plan = graph(f"https://graph.microsoft.com/v1.0/planner/plans/{PLAN}")
buckets = graph(f"https://graph.microsoft.com/v1.0/planner/plans/{PLAN}/buckets")["value"]
tasks = graph(f"https://graph.microsoft.com/v1.0/planner/plans/{PLAN}/tasks")["value"]
bucket_map = {b["id"]: b["name"].strip() for b in buckets}

for i,t in enumerate(tasks,1):
    try:
        d = graph(f"https://graph.microsoft.com/v1.0/planner/tasks/{t['id']}/details")
    except Exception as e:
        d = {"error": str(e), "checklist": {}, "description": ""}
    t["bucketName"] = bucket_map.get(t.get("bucketId"),"")
    t["details"] = d
    print(f"[{i}/{len(tasks)}] {t.get('title','')}")

out = {
    "provider": "microsoft_planner",
    "plan": plan,
    "buckets": buckets,
    "tasks": tasks
}
dest = ROOT/"data"/"planner_snapshot.json"
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"SNAPSHOT={dest}")
