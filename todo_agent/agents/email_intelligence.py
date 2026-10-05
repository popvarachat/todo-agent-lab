from todo_agent.intake.parser import extract_action_items

def analyze_email(subject: str, body: str, sender: str = "", source_ref: str = "") -> dict:
    items=extract_action_items(body,"email")
    if not items and subject:
        items=extract_action_items(subject,"email")
    enriched=[]
    for item in items:
        missing=[]
        if not item.get("owner"): missing.append("owner")
        if not item.get("due"): missing.append("due")
        confidence=1.0 - (0.2 * len(missing))
        enriched.append({
          **item,
          "sender":sender,
          "source_ref":source_ref,
          "missing":missing,
          "confidence":round(max(0.0,confidence),2),
          "recommended_action":"REVIEW_AND_PROPOSE_TASK" if confidence >= 0.8 else "REQUEST_CONTEXT"
        })
    return {
      "agent":"email_intelligence",
      "input_type":"email",
      "subject":subject,
      "items":enriched,
      "count":len(enriched)
    }
