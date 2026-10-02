import json, subprocess

class OutlookGraphSource:
    def _graph(self, url: str):
        cmd=["az.cmd","rest","--method","get","--url",url,"--output","json"]
        raw=subprocess.check_output(cmd,text=True,encoding="utf-8",errors="replace")
        return json.loads(raw)

    def recent_mail(self, top=20):
        url=("https://graph.microsoft.com/v1.0/me/messages"
             f"?$top={int(top)}&$select=id,subject,receivedDateTime,from,bodyPreview,webLink"
             "&$orderby=receivedDateTime%20desc")
        return self._graph(url).get("value",[])

    def recent_events(self, top=20):
        url=("https://graph.microsoft.com/v1.0/me/events"
             f"?$top={int(top)}&$select=id,subject,start,end,bodyPreview,webLink"
             "&$orderby=start/dateTime%20desc")
        return self._graph(url).get("value",[])
