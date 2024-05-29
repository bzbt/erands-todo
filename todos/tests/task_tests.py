import pytest

from django.contrib.auth.models import User

from todos.models import Task, Location


@pytest.mark.django_db
def test_task_model():
    user = User.objects.create_user(username="testuser", password="testpassword")
    task = Task.objects.create(
        title="Test task",
        description="Test description",
        user=user,
        weather=None,
        location=Location.objects.create(
            city="Test city", country="Test country", latitude=0.0, longitude=0.0
        ),
    )
    assert task.title == "Test task"
    assert str(task) == "Test task"
    assert task.description == "Test description"
    assert task.complete == False
    assert task.deleted == False
    assert task.user.username == "testuser"
    assert task.created is not None
    assert task.updated is not None
    assert task.public_id is not None
    assert str(task.location) == "Test city, Test country"
