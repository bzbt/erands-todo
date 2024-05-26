from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.TaskForm.as_view(), name="add_todo"),
    path("edit/<str:public_id>", views.edit, name="edit_todo"),
    path("save/", views.save, name="save_todo"),
    path("save/<str:public_id>", views.save, name="save_todo"),
]
