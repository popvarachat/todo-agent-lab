def query_tasks(result: dict, question: str):
    q=question.lower()
    rows=result.get("ranked",[])
    findings=result.get("findings",[])
    by_task={}
    for f in findings:
        by_task.setdefault(f["task_id"],set()).add(f["kind"])

    if any(k in q for k in ["overdue","เกินกำหนด","เลยกำหนด"]):
        rows=[r for r in rows if "overdue" in by_task.get(r["id"],set())]
    elif any(k in q for k in ["stale","เงียบ","ไม่คืบ","ไม่มีความคืบหน้า"]):
        rows=[r for r in rows if "stale" in by_task.get(r["id"],set())]
    elif any(k in q for k in ["hold","พัก"]):
        rows=[r for r in rows if "hold" in r.get("bucket","").lower()]
    elif any(k in q for k in ["urgent","เร่งด่วน"]):
        rows=[r for r in rows if "urgent" in by_task.get(r["id"],set())]
    else:
        terms=[x for x in q.split() if len(x)>2]
        if terms:
            rows=[r for r in rows if any(t in r.get("title","").lower() for t in terms)]
    return rows[:10]
