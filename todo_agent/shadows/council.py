from todo_agent.shadows.rdc_shadow import review as rdc_review
from todo_agent.shadows.jev_shadow import review as jev_review

def review(summary: dict, counts: dict, proposals_count: int, provider: str, evidence_summary: dict | None=None) -> dict:
    evidence_summary=evidence_summary or {}
    state={
      "goal":"Review Todo Agent executive decision state as a shadow coprocessor",
      "provider":provider,
      "active_tasks":summary.get("active",0),
      "overdue":counts.get("overdue",0),
      "stale":counts.get("stale",0),
      "quality_issues":summary.get("quality_issues",0),
      "proposals":proposals_count,
      "evidence_summary":evidence_summary,
      "mode":"READ_SUGGEST_WITH_HUMAN_GATED_WRITE",
      "hard_policy_precedence":True,
      "human_gate":True
    }
    rdc=rdc_review(summary,counts,proposals_count)
    jev=jev_review(state)
    jev_risk=((jev.get("results") or {}).get("risk") or {}).get("selected")
    jev_evidence=((jev.get("results") or {}).get("evidence") or {}).get("selected")
    disagreement=False
    if jev_risk:
        disagreement=(rdc["recommendation"]=="PROCEED" and jev_risk in {"HIGH","HUMAN_GATE"})
    evidence_gap=(evidence_summary.get("weak",0)>0 or jev_evidence=="NO")
    return {
      "mode":"DUAL_SHADOW",
      "primary_decision_authority":"Todo Agent + Human Gate",
      "shadows":{"rdc":rdc,"jev":jev},
      "disagreement":disagreement,
      "evidence_gap":evidence_gap,
      "evidence_summary":evidence_summary,
      "policy":"Shadow outputs advise only; they never bypass hard policy or Human Gate."
    }
