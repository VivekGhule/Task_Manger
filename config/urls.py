# Task_Manager/config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main apps
    path('', include('apps.tasks.urls')),
    path('auth/', include('apps.users.urls')),
    path('meetings/', include('apps.meetings.urls')),
]
