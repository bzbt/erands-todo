from django.contrib.auth.models import User
from django.test import TestCase

from todos.models import Task


def mock_user():
    """
    Create a mock user
    """

    return User.objects.create_user(username="testuser", password="testpassword")


class TaskModelTest(TestCase):
    def test_task_model(self):
        """
        Test the Task model
        """

        task = Task.objects.create(
            title="Test task",
            description="Test description",
            user=mock_user(),
        )
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.complete, False)
        self.assertEqual(task.user.username, "testuser")
        self.assertIsNotNone(task.public_id)
        self.assertIsNotNone(task.created)
        self.assertIsNotNone(task.updated)
        self.assertEqual(str(task), "Test task")
