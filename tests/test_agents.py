import unittest
from todo_agent.models import Task
from todo_agent.agents.doctor import inspect_task as doctor
from todo_agent.agents.suggest import suggest

class AgentTests(unittest.TestCase):
    def test_doctor_and_suggest(self):
        t=Task(id="1",title="Demo")
        findings=doctor(t)
        kinds={x.kind for x in findings}
        self.assertIn("no_owner",kinds)
        self.assertIn("no_due",kinds)
        ideas=suggest(t,findings)
        self.assertTrue(any("owner" in x.lower() for x in ideas))

if __name__=="__main__":
    unittest.main()
