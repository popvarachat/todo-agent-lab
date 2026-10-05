from todo_agent.intake.parser import extract_action_items

def analyze_meeting(text: str, source_ref: str = "") -> dict:
    items=extract_action_items(text,"meeting")
    enriched=[]
    for item in items:
        missing=[]
        if not item.get("owner"): missing.append("owner")
        if not item.get("due"): missing.append("due")
        confidence=1.0 - (0.2 * len(missing))
        enriched.append({
          **item,
          "source_ref":source_ref,
          "missing":missing,
          "confidence":round(max(0.0,confidence),2),
          "recommended_action":"REVIEW_AND_PROPOSE_TASK" if confidence >= 0.8 else "REQUEST_CONTEXT"
        })
    return {
      "agent":"meeting_intelligence",
      "input_type":"meeting_text",
      "items":enriched,
      "count":len(enriched)
    }
