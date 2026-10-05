import unittest
from todo_agent.models import Task, TaskFinding
from todo_agent.agents.meeting_intelligence import analyze_meeting
from todo_agent.agents.email_intelligence import analyze_email
from todo_agent.agents.evidence_context import build_task_evidence

class IntelligenceAgentTests(unittest.TestCase):
    def test_meeting_intelligence(self):
        r=analyze_meeting("ACTION: ติดตาม DWG owner: Pop due: 2026-10-10","meeting://demo")
        self.assertEqual(r["count"],1)
        self.assertEqual(r["items"][0]["owner"],"Pop")
        self.assertEqual(r["items"][0]["recommended_action"],"REVIEW_AND_PROPOSE_TASK")

    def test_email_intelligence(self):
        r=analyze_email("Follow up","ต้องติดตามงาน owner: QC due: 2026-10-11",source_ref="mail://1")
        self.assertEqual(r["count"],1)
        self.assertEqual(r["items"][0]["source_ref"],"mail://1")

    def test_evidence_context(self):
        t=Task(id="1",title="Demo",due="2026-10-10T00:00:00Z",description="Definition of done")
        fs=[TaskFinding("1","Demo","overdue",4,"late")]
        r=build_task_evidence(t,fs)
        self.assertIn(r["evidence_quality"],{"MODERATE","STRONG"})
        self.assertGreater(r["evidence_score"],0)

if __name__=="__main__":
    unittest.main()
