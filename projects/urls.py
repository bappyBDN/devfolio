from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # The prefix '/projects/' is handled by the main urls.py, so we use an empty string here
    path('', views.project_list_view, name='project_list'),
    path('<slug:slug>/', views.project_detail_view, name='project_detail'),
]