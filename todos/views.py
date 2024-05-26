import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from todos import repository
from todos.models import Task, Location
from todos.factory import TaskFactory

task_repository = repository.TaskRepository()


@login_required(login_url="account/login/")
def index(request: HttpRequest):
    """
    Renders the home page

    @param request: The request object
    """
    return render(
        request,
        "todos/_home.html",
        {"tasks": task_repository.get_all_for_user(request.user)},
    )


@login_required(login_url="account/login/")
def add(request: HttpRequest) -> HttpResponse:
    """
    Renders the task form when adding a new task

    @param request: The request object

    @return: The HTTP response
    """
    locations = Location.objects.all()
    return render(request, "todos/_form.html", {"locations": locations})


# Edit a task
@login_required(login_url="account/login/")
def edit(request: HttpRequest, public_id: str) -> HttpResponseNotFound | HttpResponse:
    """
    Renders the task form when editing a task

    @param request: The request object
    @param public_id: The public id of the task

    @return: The HTTP response
    """
    try:
        task = task_repository.get_for_user_by_public_id(public_id, request.user)
        locations = Location.objects.all()
        return render(
            request, "todos/_form.html", {"task": task, "locations": locations}
        )
    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not found")


@login_required(login_url="account/login/")
@require_http_methods(["POST"])
def save(
    request: HttpRequest, public_id: str = None
) -> HttpResponseNotFound | HttpResponse:
    """
    Creates or updates a task and redirects to the home page

    @param request: The request object
    @param public_id: The public id of the task
    """

    errors = []
    belongs_to_user = (
        True
        if public_id is None
        else task_repository.belongs_to_user(public_id, request.user)
    )

    print("pubid " + str(belongs_to_user))
    if not belongs_to_user:
        return HttpResponseNotFound("Task not found")

    task = TaskFactory().from_post(request, public_id)

    if task.deleted:
        task.save()
        return redirect("index")

    if task.title == "":
        errors.append("Title is required")

    if errors:
        task.public_id = None
        return render(request, "todos/_form.html", {"errors": errors, "task": task})

    task.save()
    return redirect("index")
