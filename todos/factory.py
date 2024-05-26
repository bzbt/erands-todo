from django.http import HttpRequest

from todos.models import Task


class TaskFactory:
    class Meta:
        model = Task

    def from_post(self, request: HttpRequest):
        """
        Creates a Task object from a POST request

        @param request: The request object
        """
        return self.Meta.model(
            title=request.POST.get("title").strip(),
            description=request.POST.get("description").strip(),
            user=request.user,
            complete="complete" in request.POST,
        )
