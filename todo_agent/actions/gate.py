import json
from pathlib import Path
from todo_agent.actions.planner_writer import PlannerWriter
from todo_agent.audit.log import append_event
from todo_agent.actions.queue import load_queue, update_status

SUPPORTED = {"patch_task","patch_details","create_task"}

def execute_proposal(queue_path: Path, audit_path: Path, proposal_id: str, confirm: str, dry_run: bool=True):
    rows=load_queue(queue_path)
    proposal=next((x for x in rows if x["id"]==proposal_id),None)
    if not proposal:
        raise ValueError(f"Proposal not found: {proposal_id}")
    if proposal.get("status") not in ("proposed","approved"):
        raise ValueError(f"Proposal status is {proposal.get('status')}")
    action=proposal.get("action_type")
    if action not in SUPPORTED:
        raise ValueError(f"Action type is advisory only: {action}")
    payload=proposal.get("payload") or {}
    if not payload:
        raise ValueError("Write proposal has no payload")

    append_event(audit_path,"approval_attempt",{"proposal_id":proposal_id,"dry_run":dry_run})
    if dry_run:
        return {"dry_run":True,"proposal":proposal}
    if confirm != "YES":
        raise ValueError("Execution requires confirm='YES'")

    writer=PlannerWriter()
    if action=="patch_task":
        result=writer.patch_task(proposal["task_id"],payload)
    elif action=="patch_details":
        result=writer.patch_details(proposal["task_id"],payload)
    else:
        result=writer.create_task(payload)
    update_status(queue_path,proposal_id,"executed")
    append_event(audit_path,"executed",{"proposal_id":proposal_id,"task_id":proposal["task_id"],"action":action})
    return {"dry_run":False,"result":result,"proposal":proposal}
