import json, os, subprocess
from pathlib import Path

def review(state: dict) -> dict:
    local=os.environ.get("LOCALAPPDATA","")
    runtime=Path(local)/"UAIOS"/"RDC"/"rdc-jev.cmd"
    if not runtime.exists():
        return {"source":"JEV","mode":"SHADOW","status":"UNAVAILABLE","execution_authority":False}
    cmd=[str(runtime),"profile","full","--state",json.dumps(state,ensure_ascii=False,separators=(",",":"))]
    try:
        raw=subprocess.check_output(cmd,text=True,encoding="utf-8",errors="replace",timeout=25)
        data=json.loads(raw)
        return {
          "source":"JEV",
          "mode":"SHADOW",
          "status":data.get("status"),
          "model":data.get("model"),
          "accepted_for_execution":data.get("accepted_for_execution",False),
          "latency_ms":data.get("latency_ms"),
          "results":data.get("results",{}),
          "execution_authority":False
        }
    except Exception as e:
        return {"source":"JEV","mode":"SHADOW","status":"ERROR","error":str(e),"execution_authority":False}
