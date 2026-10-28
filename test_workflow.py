import os
import unittest
from workflow import WorkflowEngine

class TestWorkflowEngine(unittest.TestCase):
    def setUp(self):
        self.db_name="test_carestream.db"
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.engine=WorkflowEngine(db_path=self.db_name)
        self.admin_id=self.engine.add_user("admin_user","ADMIN")
        self.nurse_id=self.engine.add_user("nurse_user","NURSE")

    def tearDown(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_create_task_success(self):
        tid=self.engine.create_task(self.admin_id,101,"NURSE","Administer Vitals Check")
        self.assertIsNotNone(tid)

    def test_unauthorized_user_creation(self):
        with self.assertRaises(PermissionError):
            self.engine.create_task(999,101,"NURSE","Unauthorized task")

    def test_task_status_update_and_audit(self):
        tid=self.engine.create_task(self.admin_id,102,"NURSE","Draw Blood Sample")
        res=self.engine.update_task_status(self.nurse_id,tid,"COMPLETED")
        self.assertTrue(res)
        logs=self.engine.get_audit_trail("care_tasks",tid)
        self.assertEqual(len(logs),2)
        self.assertEqual(logs[0][2],"CREATE_TASK")
        self.assertEqual(logs[1][2],"UPDATE_TASK_STATUS")

if __name__=="__main__":
    unittest.main()