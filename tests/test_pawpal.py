import unittest
from pawpal_system import Task, Priority


class TestTaskMarkComplete(unittest.TestCase):

    # setUp method to create a Task instance before each test
    def setUp(self):
        self.task = Task(
            id="t1",
            description="Walk the dog",
            duration_minutes=30,
            priority=Priority.HIGH
        )

    def test_initial_status_is_false(self):
        self.assertFalse(self.task.get_completion_status())

    def test_mark_complete_sets_status_to_true(self):
        self.task.mark_complete()
        self.assertTrue(self.task.get_completion_status())

    def test_mark_complete_is_idempotent(self):
        self.task.mark_complete()
        self.task.mark_complete()
        self.assertTrue(self.task.get_completion_status())

    def test_completion_status_field_updated_directly(self):
        self.task.mark_complete()
        self.assertTrue(self.task.completion_status)

    def test_mark_incomplete_sets_status_to_false(self):
        self.task.mark_complete()  # First mark it complete
        self.task.mark_incomplete()  # Then mark it incomplete
        self.assertFalse(self.task.get_completion_status())
        
if __name__ == "__main__":
    unittest.main()
