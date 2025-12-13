from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("tasks", views.tasks_collection, name="tasks_collection"),        # GET, POST
    path("tasks/<str:task_id>", views.task_detail, name="task_detail"),    # GET, PUT, DELETE
    path("tasks/completed/all", views.clear_completed, name="clear_completed"),  # DELETE
    path("stats", views.get_stats, name="stats"),
]
