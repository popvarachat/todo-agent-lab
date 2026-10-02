import re, uuid
from pathlib import Path

DATE_RE=re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
OWNER_RE=re.compile(r"(?:owner|ผู้รับผิดชอบ)\s*[:=-]\s*(.+?)(?=\s+(?:due|กำหนด)\s*[:=-]|[|;]|$)",re.I)
DUE_RE=re.compile(r"(?:due|กำหนด)\s*[:=-]\s*(.+?)(?=\s+(?:owner|ผู้รับผิดชอบ)\s*[:=-]|[|;]|$)",re.I)

def extract_action_items(text: str, source: str):
    items=[]
    for raw in text.splitlines():
        line=raw.strip(" -*\t")
        if not line:
            continue
        low=line.lower()
        looks_action=any(k in low for k in ["action","todo","ต้อง","ติดตาม","ดำเนินการ","follow up","follow-up"])
        if not looks_action:
            continue
        om=OWNER_RE.search(line)
        dm=DUE_RE.search(line)
        owner=om.group(1).strip() if om else None
        due=dm.group(1).strip() if dm else None
        if not due:
            m=DATE_RE.search(line)
            due=m.group(1) if m else None
        items.append({
          "id":uuid.uuid4().hex[:12],
          "title":line,
          "owner":owner,
          "due":due,
          "source":source,
          "status":"draft"
        })
    return items

def parse_file(path: str, source: str):
    return extract_action_items(Path(path).read_text(encoding="utf-8-sig"), source)
