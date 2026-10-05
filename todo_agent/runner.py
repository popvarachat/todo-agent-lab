import json
from pathlib import Path
from collections import Counter

from todo_agent.providers.planner import PlannerProvider
from todo_agent.providers.json_file import JsonFileProvider
from todo_agent.providers.microsoft_todo import MicrosoftToDoProvider
from todo_agent.agents.radar import inspect_task as radar_inspect
from todo_agent.agents.doctor import inspect_task as doctor_inspect
from todo_agent.agents.hold import inspect_task as hold_inspect
from todo_agent.agents.suggest import suggest
from todo_agent.agents.weekly import build_weekly_summary
from todo_agent.agents.followup import build_message
from todo_agent.agents.evidence_context import build_task_evidence
from todo_agent.actions.models import ActionProposal
from todo_agent.actions.queue import proposal_id, save_queue
from todo_agent.shadows.council import review as shadow_review

def build_provider(cfg):
    name=cfg.get("provider","microsoft_planner")
    if name=="json_file":
        return JsonFileProvider(cfg["data_path"])
    if name=="microsoft_todo":
        return MicrosoftToDoProvider(cfg.get("list_id","all"))
    return PlannerProvider(cfg["plan_id"])

def run(config_path: str):
    root=Path(config_path).resolve().parents[1]
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8-sig"))
    provider=build_provider(cfg)
    tasks=provider.list_tasks()
    active=[t for t in tasks if t.percent_complete < 100]

    findings=[]
    task_findings={}
    for t in active:
        fs=[]
        fs += radar_inspect(t,cfg.get("stale_days",14),cfg.get("due_soon_days",7))
        fs += doctor_inspect(t)
        fs += hold_inspect(t)
        findings += fs
        task_findings[t.id]=fs

    evidence_by_task={}
    for t in active:
        evidence_by_task[t.id]=build_task_evidence(t,task_findings.get(t.id,[]))

    evidence_counts=Counter(x["evidence_quality"] for x in evidence_by_task.values())

    counts=Counter(f.kind for f in findings)
    score={}
    for f in findings:
        score[f.task_id]=score.get(f.task_id,0)+f.severity
    ranked=sorted(active,key=lambda t:(-score.get(t.id,0),t.due or "9999"))

    proposals=[]
    for t in ranked:
        fs=task_findings.get(t.id,[])
        msg=build_message(t,fs)
        if msg:
            proposals.append(ActionProposal(
                id=proposal_id(),task_id=t.id,title=t.title,
                action_type="follow_up",reason="; ".join(f.kind for f in fs if f.kind in ("overdue","stale")),
                risk="medium",payload={"message":msg}
            ))
        if "hold" in t.bucket.lower():
            proposals.append(ActionProposal(
                id=proposal_id(),task_id=t.id,title=t.title,
                action_type="review_hold",reason="HOLD governance review",
                risk="low",payload={}
            ))

    weekly=build_weekly_summary(len(active),findings)
    evidence_summary={
      "strong":evidence_counts.get("STRONG",0),
      "moderate":evidence_counts.get("MODERATE",0),
      "weak":evidence_counts.get("WEAK",0)
    }
    shadow=shadow_review(
      weekly,dict(counts),len(proposals),provider.provider_name(),evidence_summary
    ) if cfg.get("shadow_mode",True) else {"mode":"OFF"}

    result={
      "provider":provider.provider_name(),
      "active_tasks":len(active),
      "weekly_summary":weekly,
      "evidence_summary":evidence_summary,
      "evidence_by_task":evidence_by_task,
      "shadow_review":shadow,
      "counts":dict(counts),
      "ranked":[{"id":t.id,"title":t.title,"bucket":t.bucket,
                 "score":score.get(t.id,0),"due":t.due,
                 "suggestions":suggest(t,task_findings.get(t.id,[]))}
                for t in ranked],
      "findings":[f.__dict__ for f in findings],
      "proposals":[p.__dict__ for p in proposals]
    }

    outdir=root/"output"
    outdir.mkdir(exist_ok=True)
    (outdir/"agent_result.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    save_queue(outdir/"proposals.json",proposals)

    lines=["# Todo Agent Report","",
           f"Provider: **{provider.provider_name()}**",
           f"Active tasks: **{len(active)}**","",
           "## Findings"]
    for k,v in sorted(counts.items()):
        lines.append(f"- {k}: **{v}**")
    lines += ["","## Weekly Brief"]
    for k,v in result["weekly_summary"].items():
        lines.append(f"- {k}: **{v}**")
    lines += ["","## Evidence Context",
              f"- Strong evidence: **{evidence_summary['strong']}**",
              f"- Moderate evidence: **{evidence_summary['moderate']}**",
              f"- Weak evidence: **{evidence_summary['weak']}**"]
    lines += ["","## Morning Radar"]
    for t in ranked[:12]:
        ideas=suggest(t,task_findings.get(t.id,[]))
        lines.append(f"- **{t.title}** | {t.bucket} | score {score.get(t.id,0)} | due {t.due or '-'}")
        for idea in ideas[:3]:
            lines.append(f"  - Suggest: {idea}")
    lines += ["","## Shadow Decision Council",
              f"- Mode: **{shadow.get('mode','OFF')}**",
              f"- Primary authority: **{shadow.get('primary_decision_authority','Todo Agent + Human Gate')}**"]
    if shadow.get("shadows"):
        rdc=shadow["shadows"].get("rdc",{})
        jev=shadow["shadows"].get("jev",{})
        lines += [f"- RDC Shadow: **{rdc.get('recommendation','N/A')}** · score {rdc.get('score','-')}",
                  f"- JEV Shadow: **{jev.get('status','N/A')}** · model {jev.get('model','-')} · authority=false"]
    lines += ["","## Approval Queue",f"- Proposed actions: **{len(proposals)}**",
              "- Follow-up and HOLD items remain advisory until explicitly approved.",
              "","_READ/SUGGEST mode: no live task was modified._"]
    (outdir/"agent_report.md").write_text("\n".join(lines),encoding="utf-8")
    return result
