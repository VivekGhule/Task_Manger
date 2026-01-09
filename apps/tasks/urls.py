# Task_Manager\apps\tasks\urls.py
from django.urls import path
from .views import dashboard, tasks_api, task_detail_api

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("api/tasks/", tasks_api),
    path("api/tasks/<str:task_id>/", task_detail_api),
]
