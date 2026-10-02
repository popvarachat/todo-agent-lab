import argparse, json, uuid
from pathlib import Path

from todo_agent.runner import run
from todo_agent.agents.conversation import query_tasks
from todo_agent.intake.parser import parse_file
from todo_agent.actions.queue import load_queue
from todo_agent.actions.gate import execute_proposal

def root_from_config(config):
    return Path(config).resolve().parents[1]

def cmd_analyze(args):
    result=run(args.config)
    print(json.dumps({"active_tasks":result["active_tasks"],"counts":result["counts"],
                      "weekly_summary":result["weekly_summary"],
                      "proposals":len(result["proposals"])},
                     ensure_ascii=False,indent=2))

def cmd_query(args):
    root=root_from_config(args.config)
    result=json.loads((root/"output"/"agent_result.json").read_text(encoding="utf-8-sig"))
    rows=query_tasks(result,args.question)
    print(json.dumps(rows,ensure_ascii=False,indent=2))

def cmd_intake(args):
    root=root_from_config(args.config)
    items=parse_file(args.file,args.kind)
    dest=root/"output"/f"{args.kind}_intake.json"
    dest.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"items":len(items),"output":str(dest)},ensure_ascii=False,indent=2))

def cmd_propose_write(args):
    root=root_from_config(args.config)
    queue=root/"output"/"proposals.json"
    rows=load_queue(queue)
    if args.payload_file:
        payload=json.loads(Path(args.payload_file).read_text(encoding="utf-8-sig"))
    else:
        payload=json.loads(args.payload)
    row={
      "id":uuid.uuid4().hex[:12],
      "task_id":args.task_id,
      "title":args.title or args.task_id,
      "action_type":args.action_type,
      "reason":args.reason,
      "risk":"high",
      "payload":payload,
      "status":"proposed"
    }
    rows.append(row)
    queue.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(row,ensure_ascii=False,indent=2))

def cmd_approve(args):
    root=root_from_config(args.config)
    result=execute_proposal(
      root/"output"/"proposals.json",
      root/"output"/"audit.jsonl",
      args.proposal_id,
      confirm=args.confirm,
      dry_run=not args.execute
    )
    print(json.dumps(result,ensure_ascii=False,indent=2))

def build_parser():
    ap=argparse.ArgumentParser(prog="todo-agent")
    ap.add_argument("--config",default="config/settings.json")
    sub=ap.add_subparsers(dest="command")

    p=sub.add_parser("analyze"); p.set_defaults(func=cmd_analyze)
    p=sub.add_parser("query"); p.add_argument("question"); p.set_defaults(func=cmd_query)
    p=sub.add_parser("intake")
    p.add_argument("--kind",choices=["meeting","email"],required=True)
    p.add_argument("--file",required=True); p.set_defaults(func=cmd_intake)

    p=sub.add_parser("propose-write")
    p.add_argument("--task-id",required=True)
    p.add_argument("--action-type",choices=["patch_task","patch_details","create_task"],required=True)
    payload_group=p.add_mutually_exclusive_group(required=True)
    payload_group.add_argument("--payload",help='JSON payload, e.g. {"priority":3}')
    payload_group.add_argument("--payload-file",help="Path to JSON payload file")
    p.add_argument("--reason",required=True)
    p.add_argument("--title",default="")
    p.set_defaults(func=cmd_propose_write)

    p=sub.add_parser("approve")
    p.add_argument("proposal_id")
    p.add_argument("--execute",action="store_true")
    p.add_argument("--confirm",default="")
    p.set_defaults(func=cmd_approve)
    return ap

def main():
    ap=build_parser()
    args=ap.parse_args()
    if not args.command:
        args.command="analyze"
        args.func=cmd_analyze
    args.func(args)

if __name__=="__main__":
    main()
