def build_task_evidence(task, findings, intake_refs=None) -> dict:
    evidence=[]
    raw=task.raw or {}
    if task.due:
        evidence.append({"kind":"due_date","value":task.due,"weight":2})
    if task.assignments:
        evidence.append({"kind":"owner","value":list(task.assignments.keys()),"weight":2})
    if (task.description or "").strip():
        evidence.append({"kind":"description","value":task.description[:500],"weight":1})
    if task.checklist:
        evidence.append({"kind":"checklist","value":len(task.checklist),"weight":1})
    if raw.get("createdDateTime"):
        evidence.append({"kind":"created","value":raw.get("createdDateTime"),"weight":1})
    for f in findings:
        evidence.append({"kind":"finding","value":f.kind,"message":f.message,"weight":1})
    for ref in intake_refs or []:
        evidence.append({"kind":"source_ref","value":ref,"weight":2})

    score=sum(e.get("weight",1) for e in evidence)
    quality="STRONG" if score >= 8 else "MODERATE" if score >= 4 else "WEAK"
    return {
      "agent":"evidence_context",
      "task_id":task.id,
      "evidence_score":score,
      "evidence_quality":quality,
      "evidence":evidence
    }
