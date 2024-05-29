from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="task_list"),
    path("task/", views.manage_task, name="create_task"),
    path("task/<str:public_id>", views.manage_task, name="update_task"),
    path("task/weather/", views.get_weather, name="location_weather"),
]
