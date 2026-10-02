import unittest, tempfile
from pathlib import Path
from todo_agent.models import Task, TaskFinding
from todo_agent.agents.hold import inspect_task as hold
from todo_agent.agents.followup import build_message
from todo_agent.agents.conversation import query_tasks
from todo_agent.intake.parser import extract_action_items

class WorkflowTests(unittest.TestCase):
    def test_hold_governance(self):
        t=Task(id="h1",title="Hold demo",bucket="ETC. & Hold",description="")
        kinds={x.kind for x in hold(t)}
        self.assertIn("hold_reason",kinds)
        self.assertIn("resume_condition",kinds)
        self.assertIn("review_date",kinds)

    def test_followup(self):
        t=Task(id="1",title="Demo")
        fs=[TaskFinding("1","Demo","overdue",4,"late")]
        self.assertIn("ติดตามงาน",build_message(t,fs))

    def test_intake(self):
        rows=extract_action_items("ACTION: ทำรายงาน owner: Pop due: 2026-10-10","meeting")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["owner"],"Pop")

    def test_query(self):
        result={
          "ranked":[{"id":"1","title":"Late task","bucket":"Monitor"}],
          "findings":[{"task_id":"1","kind":"overdue"}]
        }
        self.assertEqual(len(query_tasks(result,"งานเกินกำหนด")),1)

if __name__=="__main__":
    unittest.main()
