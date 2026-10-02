import argparse, json
from todo_agent.runner import run

def main():
    ap=argparse.ArgumentParser(prog="todo-agent")
    ap.add_argument("--config",default="config/settings.json")
    args=ap.parse_args()
    result=run(args.config)
    print(json.dumps({
      "active_tasks":result["active_tasks"],
      "counts":result["counts"]
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
