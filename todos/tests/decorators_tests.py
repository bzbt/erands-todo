import pytest
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.test import RequestFactory

import todos.views
from todos.decorators.tasks import task_create_or_update
from todos.models import Task


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def task(user, db):
    return Task.objects.create(
        title='Test Task',
        description='Test Description',
        complete=False,
        deleted=False,
        public_id='4d092ea9-1d18-4edb-b23a-99723690b8a8',
        user=user
    )


@pytest.fixture
def request_factory(**kwargs):
    return RequestFactory(**kwargs)


def mock_view(request, *args, **kwargs):
    return todos.views.manage_task(request, *args, **kwargs)


def test_task_create_or_update_with_public_id_found(request_factory, user, task):
    request = request_factory.get('/fake-url/' + task.public_id)
    request.user = user
    request.kwargs = {'public_id': task.public_id}
    wrapped_view = task_create_or_update(mock_view)
    response = wrapped_view(request, public_id=task.public_id, task=task)

    assert response.status_code == 200


def test_task_create_or_update_with_public_id_not_found(request_factory, user):
    request = request_factory.get('/fake-url/')
    request.user = user

    wrapped_view = task_create_or_update(mock_view)

    with pytest.raises(Http404):
        wrapped_view(request, public_id='17318b9e-4475-4ffb-bb85-5d4aa81da2d7')


def test_task_create_or_update_without_public_id(request_factory, user):
    request = request_factory.get('/fake-url/')
    request.user = user

    wrapped_view = task_create_or_update(mock_view)
    response = wrapped_view(request)

    assert response.status_code == 200
