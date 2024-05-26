from django.contrib.auth.models import User

from todos.models import Task


class TaskRepository:
    """
    Task repository class
    """

    class Meta:
        """
        Meta class
        """

        model = Task.objects

    def get_by_public_id(self, public_id: str):
        """
        Get a task by public id

        @param self: The TaskRepository object
        @param public_id: The public id of the task
        """
        return self.Meta.model.get(public_id=public_id, deleted=False)

    def get_all_for_user(self, user: User):
        """
        Get all tasks by user

        @param self: The TaskRepository object
        @param user: The user object
        """
        return self.Meta.model.all().filter(user=user, deleted=False)

    def get_for_user_by_public_id(self, public_id: str, user: User):
        """
        Get a task by public id for a user

        @param self: The TaskRepository object
        @param public_id: The public id of the task
        @param user: The user object
        """
        return self.Meta.model.get(public_id=public_id, user=user, deleted=False)
