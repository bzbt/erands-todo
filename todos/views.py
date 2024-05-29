import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from todos.decorators.tasks import task_create_or_update
from todos.forms import TaskForm, WeatherForm
from todos.models import Task, Location
from todos.utils import refresh_weather


@login_required(login_url="account/login/")
def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page

    @param request: The request object
    """
    return render(
        request,
        "todos/_home.html",
        {"tasks": Task.objects.all().filter(user=request.user, deleted=False)},
    )


@login_required(login_url="account/login/")
@task_create_or_update
def manage_task(request: HttpRequest, **kwargs) -> HttpResponse:
    """
    Creates or updates a task and redirects to the home page

    Args:
        request  (HttpRequest): The HTTP request object
        **kwargs (Any):           Additional keyword arguments

    Returns:
        HttpResponse: The HTTP response
    """
    task: Task = kwargs.get("task")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.data.get('delete') is not None:
            task.deleted = True
            task.save(update_fields=['deleted'])
            return redirect('task_list')
        if form.data.get('complete') is not None:
            task.complete = not task.complete
            task.save(update_fields=['complete'])
            return redirect('update_task', task.public_id)

        weather_data = json.loads(request.POST.get('weather'))
        weather_form = WeatherForm(weather_data)
        if form.is_valid() and weather_form.is_valid():
            task = form.save(commit=False)
            task.weather = weather_form.save()
            task.user = request.user
            task.save()

            return redirect('task_list')
        else:
            return render(
                request, 'todos/_form.html',
                {'form': TaskForm(instance=task), 'weather_errors': weather_form.errors}
            )
    else:
        form = TaskForm(instance=task, disable_all=task.complete)

    return render(
        request,
        'todos/_form.html',
        {
            'form': form,
            "weather": task.weather,
            "location": task.location,
        }
    )


@login_required(login_url="account/login/")
@require_http_methods(["POST"])
def get_weather(request: HttpRequest) -> JsonResponse:
    """
    Returns assigned weather data for a task or location.

    Args:
        request (HttpRequest): The request object

    Returns:
        JsonResponse: The HTTP response
    """
    data = json.loads(request.body)
    location_id = data.get("location_id")
    task_id = data.get("task_id")
    location = get_object_or_404(Location, id=location_id)
    task = get_object_or_404(Task, public_id=task_id, user=request.user) if task_id else None

    if task and task.complete:
        return JsonResponse({"error": "Task is complete"}, status=400)

    try:
        weather = refresh_weather(location, task)
        return JsonResponse(weather.as_dictionary())
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=404)
