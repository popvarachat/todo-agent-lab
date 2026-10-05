import unittest
from todo_agent.shadows.rdc_shadow import review

class ShadowTests(unittest.TestCase):
    def test_rdc_shadow_is_advisory(self):
        r=review({"quality_issues":4},{"overdue":2,"stale":3},5)
        self.assertEqual(r["mode"],"SHADOW")
        self.assertFalse(r["execution_authority"])
        self.assertEqual(r["recommendation"],"HUMAN_REVIEW")

if __name__=="__main__":
    unittest.main()
