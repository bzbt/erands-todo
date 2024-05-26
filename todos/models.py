import uuid

from django.db import models


# Represents a task that needs to be done
class Task(models.Model):
    public_id = models.UUIDField(
        default=uuid.uuid4, editable=False, db_comment="Public identifier of the task"
    )
    title = models.CharField(max_length=200, db_comment="Title of the task")
    description = models.TextField(blank=True, db_comment="Description of the task")
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, db_comment="User who created the task"
    )
    complete = models.BooleanField(
        default=False, db_comment="Whether the task is complete"
    )
    deleted = models.BooleanField(
        default=False, db_comment="Whether the task is deleted"
    )
    created = models.DateTimeField(
        auto_now_add=True, db_comment="Date and time the task was created"
    )
    updated = models.DateTimeField(
        auto_now=True, db_comment="Date and time the task was last updated"
    )

    def __str__(self):
        return self.title
