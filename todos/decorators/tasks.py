from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from todos.models import Task


def task_create_or_update(requested_view):
    """Decorator to handle Task objects based on a public ID.

    Args:
        requested_view: The view function to wrap.
    """
    def _wrapped_view(request: HttpRequest, *args, **kwargs):
        """
        Wraps a view function to handle Task objects based on a public ID.

        Args:
            request  (HttpRequest): The HTTP request object.
            *args    (tuple):       Additional positional arguments passed to the view.
            **kwargs (tuple):       Keyword arguments passed to the view. It expects a 'public_id' key optionally.

        Returns:
            The response from the view.
        """
        pid = kwargs.get('public_id')
        if pid:
            task = get_object_or_404(Task, public_id=pid, user=request.user)
        else:
            task = Task()
        kwargs['task']: Task = task
        response = requested_view(request, *args, **kwargs)
        return response

    return _wrapped_view
