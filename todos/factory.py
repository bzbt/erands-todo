from django.contrib.auth.models import User
from django.http import HttpRequest

from todos.models import Task, Location


def get_location(location_id: int) -> Location | None:
    """
    Get a Location object by ID

    @param self: The TaskFactory object
    @param location_id: The location ID

    @return: The Location object or None
    """
    try:
        return location_id and Location.objects.get(id=location_id) or None
    except Location.DoesNotExist:
        return None


class TaskFactory:
    class Meta:
        model = Task

    def from_post(self, request: HttpRequest, public_id: str | None) -> Task:
        """
        Creates a Task object from a POST request

        @param request: The request object
        @param public_id: The public ID of the task

        @return: The Task object
        """
        task = Task() if public_id is None else Task.objects.get(public_id=public_id)
        task.title = request.POST.get("title").strip()
        task.description = request.POST.get("description").strip()
        task.complete = "complete" in request.POST
        task.deleted = "delete" in request.POST
        task.location = get_location(request.POST.get("location_id"))
        task.user = request.user

        return task
