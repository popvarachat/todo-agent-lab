import json, os, subprocess, urllib.request

class GraphClient:
    def __init__(self):
        env=os.environ.copy()
        env["PYTHONUTF8"]="1"
        env["PYTHONIOENCODING"]="utf-8"
        self.token=subprocess.check_output(
            ["az.cmd","account","get-access-token","--resource-type","ms-graph",
             "--query","accessToken","-o","tsv"],
            text=True,encoding="utf-8",errors="strict",env=env,
            stderr=subprocess.DEVNULL
        ).strip()

    def get(self, url: str):
        req=urllib.request.Request(
            url,
            headers={
              "Authorization":f"Bearer {self.token}",
              "Accept":"application/json"
            },
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
