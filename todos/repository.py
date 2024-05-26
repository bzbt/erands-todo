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

    def belongs_to_user(self, public_id: str, user: User) -> bool:
        """
        Check if a task exists and belongs to a user

        @param self: The TaskRepository object
        @param public_id: The public id of the task
        @param user: The user object

        @return: True if the task exists and belongs to the user, False otherwise
        """
        return self.Meta.model.filter(public_id=public_id, user=user).exists()

    def get_all_for_user(self, user: User) -> list[Task]:
        """
        Get all tasks by user

        @param self: The TaskRepository object
        @param user: The user object

        @return: A list of tasks for the user
        """
        return self.Meta.model.all().filter(user=user, deleted=False)

    def get_for_user_by_public_id(self, public_id: str, user: User) -> Task:
        """
        Get a task by public id for a user

        @param self: The TaskRepository object
        @param public_id: The public id of the task
        @param user: The user object

        @return: The task object
        """
        return self.Meta.model.get(public_id=public_id, user=user, deleted=False)
