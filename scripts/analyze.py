import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT/"config"/"settings.json").read_text(encoding="utf-8"))
SNAP = json.loads((ROOT/"data"/"planner_snapshot.json").read_text(encoding="utf-8"))
NOW = datetime.now(timezone.utc)
STALE_DAYS = CFG.get("stale_days",14)
DUE_SOON = CFG.get("due_soon_days",7)

def dt(s):
    if not s: return None
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def last_activity(t):
    dates=[dt(t.get("createdDateTime"))]
    for item in t.get("details",{}).get("checklist",{}).values():
        dates.append(dt(item.get("lastModifiedDateTime")))
    return max([x for x in dates if x], default=None)

rows=[]
for t in SNAP["tasks"]:
    if t.get("percentComplete")==100: continue
    due=dt(t.get("dueDateTime"))
    last=last_activity(t)
    overdue=bool(due and due < NOW)
    due_soon=bool(due and NOW <= due <= NOW+timedelta(days=DUE_SOON))
    stale=bool(last and NOW-last >= timedelta(days=STALE_DAYS))
    doctor=[]
    if not t.get("assignments"): doctor.append("No owner")
    if not due: doctor.append("No due date")
    if not t.get("details",{}).get("description","").strip(): doctor.append("No description")
    if t.get("checklistItemCount",0)==0: doctor.append("No checklist")
    score=(4 if overdue else 0)+(2 if stale else 0)+(2 if t.get("priority",5)<=1 else 0)+(1 if due_soon else 0)
    rows.append({
      "id":t["id"],"title":t.get("title",""),"bucket":t.get("bucketName",""),
      "due":t.get("dueDateTime"),"last_activity":last.isoformat() if last else None,
      "overdue":overdue,"due_soon":due_soon,"stale":stale,
      "doctor":doctor,"score":score
    })

rows.sort(key=lambda x:(-x["score"], x["due"] or "9999"))
summary={
 "generated_utc":NOW.isoformat(),"plan":SNAP["plan"]["title"],
 "active":len(rows),"overdue":sum(x["overdue"] for x in rows),
 "stale":sum(x["stale"] for x in rows),
 "due_soon":sum(x["due_soon"] for x in rows),
 "task_doctor_issues":sum(bool(x["doctor"]) for x in rows)
}
(ROOT/"output"/"analysis.json").write_text(
 json.dumps({"summary":summary,"tasks":rows},ensure_ascii=False,indent=2),encoding="utf-8")

lines=[f"# Todo Agent Pilot — {summary['plan']}","",
 f"- Active: **{summary['active']}**",
 f"- Overdue: **{summary['overdue']}**",
 f"- Stale >={STALE_DAYS} days: **{summary['stale']}**",
 f"- Due soon <={DUE_SOON} days: **{summary['due_soon']}**",
 f"- Task Doctor issues: **{summary['task_doctor_issues']}**","",
 "## Morning Radar"]
for x in rows[:12]:
    flags=[]
    if x["overdue"]: flags.append("OVERDUE")
    if x["stale"]: flags.append("STALE")
    if x["due_soon"]: flags.append("DUE-SOON")
    lines.append(f"- **{x['title']}** | {x['bucket']} | score {x['score']} | {', '.join(flags) or 'WATCH'}")

lines += ["","## Task Doctor"]
for x in [r for r in rows if r["doctor"]][:12]:
    lines.append(f"- **{x['title']}** — {', '.join(x['doctor'])}")

lines += ["","## Reusable Architecture",
 "Planner Adapter -> Canonical Task Model -> Agent Rules -> Human Gate -> Output/Action",
 "",
 "Current pilot is READ-ONLY. No Planner task is modified."
]
(ROOT/"output"/"pilot_report.md").write_text("\n".join(lines),encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False,indent=2))
print("REPORT="+str(ROOT/"output"/"pilot_report.md"))
