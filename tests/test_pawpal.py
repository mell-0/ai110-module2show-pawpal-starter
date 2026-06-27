import unittest
from pawpal_system import Task, Priority, Pet


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


class TestPetAddTask(unittest.TestCase):

    # setUp method to create a Pet instance before each test with one task
    def setUp(self):
        self.pet = Pet(id="p1", name="Buddy", species="Dog")
        self.task = Task(
            id="t1",
            description="Walk the dog",
            duration_minutes=30,
            priority=Priority.HIGH
        )

    # test that adding a task increases the number of tasks for the pet by 1
    def test_add_task_increases_task_count(self):
        count_before = len(self.pet.get_tasks())
        self.pet.add_task(self.task)
        count_after = len(self.pet.get_tasks())
        self.assertEqual(count_after, count_before + 1)


if __name__ == "__main__":
    unittest.main()
