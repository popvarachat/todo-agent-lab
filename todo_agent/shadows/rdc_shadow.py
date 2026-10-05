def review(summary: dict, findings_count: dict, proposals_count: int) -> dict:
    risks=[]
    score=100
    overdue=int(findings_count.get("overdue",0))
    stale=int(findings_count.get("stale",0))
    quality=int(summary.get("quality_issues",0))
    if overdue:
        risks.append(f"{overdue} overdue task(s)")
        score-=min(25,overdue)
    if stale:
        risks.append(f"{stale} stale task(s)")
        score-=min(20,stale//2)
    if quality:
        risks.append(f"{quality} task quality issue(s)")
        score-=min(20,quality//2)
    if proposals_count:
        risks.append(f"{proposals_count} proposed action(s) awaiting controlled handling")
    score=max(0,score)
    return {
      "source":"RDC",
      "mode":"SHADOW",
      "role":"operational_feasibility_and_execution_risk",
      "score":score,
      "recommendation":"HUMAN_REVIEW" if risks else "PROCEED",
      "risks":risks,
      "execution_authority":False
    }
