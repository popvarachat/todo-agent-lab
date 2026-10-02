import json, subprocess

class PlannerWriter:
    def __init__(self):
        pass

    def _run(self, args):
        cmd=["az.cmd","rest"]+args+["--output","json"]
        raw=subprocess.check_output(cmd,text=True,encoding="utf-8",errors="replace")
        return json.loads(raw) if raw.strip() else {}

    def get_task(self, task_id: str):
        return self._run(["--method","get","--url",f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}"])

    def get_details(self, task_id: str):
        return self._run(["--method","get","--url",f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details"])

    def patch_task(self, task_id: str, payload: dict):
        current=self.get_task(task_id)
        etag=current.get("@odata.etag")
        body=json.dumps(payload,ensure_ascii=False)
        return self._run(["--method","patch","--url",f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}",
                          "--headers",f"If-Match={etag}","Content-Type=application/json","--body",body])

    def patch_details(self, task_id: str, payload: dict):
        current=self.get_details(task_id)
        etag=current.get("@odata.etag")
        body=json.dumps(payload,ensure_ascii=False)
        return self._run(["--method","patch","--url",f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}/details",
                          "--headers",f"If-Match={etag}","Content-Type=application/json","--body",body])

    def create_task(self, payload: dict):
        body=json.dumps(payload,ensure_ascii=False)
        return self._run(["--method","post","--url","https://graph.microsoft.com/v1.0/planner/tasks",
                          "--headers","Content-Type=application/json","--body",body])
