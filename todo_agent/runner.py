import json
from pathlib import Path
from collections import Counter
from todo_agent.providers.planner import PlannerProvider
from todo_agent.providers.json_file import JsonFileProvider
from todo_agent.providers.microsoft_todo import MicrosoftToDoProvider
from todo_agent.agents.radar import inspect_task as radar_inspect
from todo_agent.agents.doctor import inspect_task as doctor_inspect
from todo_agent.agents.suggest import suggest
from todo_agent.agents.weekly import build_weekly_summary

def run(config_path: str):
    root = Path(config_path).resolve().parents[1]
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8-sig"))
    provider_name = cfg.get("provider","microsoft_planner")
    if provider_name == "json_file":
        provider = JsonFileProvider(cfg["data_path"])
    elif provider_name == "microsoft_todo":
        provider = MicrosoftToDoProvider(cfg.get("list_id","all"))
    else:
        provider = PlannerProvider(cfg["plan_id"])
    tasks = provider.list_tasks()
    active = [t for t in tasks if t.percent_complete < 100]

    findings=[]
    for t in active:
        findings += radar_inspect(t,cfg.get("stale_days",14),cfg.get("due_soon_days",7))
        findings += doctor_inspect(t)

    counts=Counter(f.kind for f in findings)
    score={}
    for f in findings:
        score[f.task_id]=score.get(f.task_id,0)+f.severity
    ranked=sorted(active,key=lambda t:(-score.get(t.id,0),t.due or "9999"))

    task_findings={}
    for f in findings:
        task_findings.setdefault(f.task_id,[]).append(f)
    result={
      "provider":provider.provider_name(),
      "active_tasks":len(active),
      "weekly_summary":build_weekly_summary(len(active),findings),
      "counts":dict(counts),
      "ranked":[{"id":t.id,"title":t.title,"bucket":t.bucket,
                 "score":score.get(t.id,0),"due":t.due,
                 "suggestions":suggest(t,task_findings.get(t.id,[]))}
                for t in ranked],
      "findings":[f.__dict__ for f in findings]
    }
    outdir=root/"output"
    outdir.mkdir(exist_ok=True)
    (outdir/"agent_result.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Todo Agent Report","",
           f"Provider: **{provider.provider_name()}**",
           f"Active tasks: **{len(active)}**","",
           "## Findings"]
    for k,v in sorted(counts.items()):
        lines.append(f"- {k}: **{v}**")
    lines += ["","## Weekly Brief"]
    for k,v in result["weekly_summary"].items():
        lines.append(f"- {k}: **{v}**")
    lines += ["","## Morning Radar"]
    for t in ranked[:12]:
        ideas=suggest(t,task_findings.get(t.id,[]))
        lines.append(f"- **{t.title}** | {t.bucket} | score {score.get(t.id,0)} | due {t.due or '-'}")
        for idea in ideas[:3]:
            lines.append(f"  - Suggest: {idea}")
    lines += ["","_Read-only pilot: no task was changed._"]
    (outdir/"agent_report.md").write_text("\n".join(lines),encoding="utf-8")
    return result
