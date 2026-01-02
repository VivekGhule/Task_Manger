from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('api/meetings/', views.meeting_list_create, name='meeting-list-create'),
    path("api/meetings/<str:meeting_id>/", views.meeting_detail),
    
]