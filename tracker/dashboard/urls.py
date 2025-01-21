from django.urls import path

from users.urls import app_name
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('example_dashboard/', views.example_dashboard, name='example_dashboard')
]