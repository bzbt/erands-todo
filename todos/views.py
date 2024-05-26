import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from todos import repository
from todos.models import Task
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


class TaskForm(TemplateView):
    """
    Renders the task form when adding a new task
    """

    login_required(login_url="account/login/")
    template_name = "todos/_form.html"


# Edit a task
@login_required(login_url="account/login/")
def edit(request: HttpRequest, public_id: str):
    """
    Renders the task form when editing a task

    @param request: The request object
    @param public_id: The public id of the task
    """

    try:
        task = task_repository.get_for_user_by_public_id(public_id, request.user)
        return render(request, "todos/_form.html", {"task": task})
    except Task.DoesNotExist:
        return HttpResponseNotFound("Task not found")


@login_required(login_url="account/login/")
@require_http_methods(["POST"])
def save(request: HttpRequest, public_id: str = None):
    """
    Creates or updates a task and redirects to the home page

    @param request: The request object
    @param public_id: The public id of the task
    """

    errors = []
    task = public_id and task_repository.get_by_public_id(public_id) or Task()
    if public_id and task.user != request.user:
        return HttpResponseNotFound("Task not found")

    task = TaskFactory().from_post(request)
    if "delete" in request.POST:
        task.deleted = True
        task.save()
        return redirect("index")

    if request.POST["title"] == "":
        errors.append("Title is required")

    if errors:
        task.public_id = None
        return render(request, "todos/_form.html", {"errors": errors, "task": task})

    task.save()
    return redirect("index")
