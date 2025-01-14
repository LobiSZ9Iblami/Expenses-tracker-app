from django.urls import path

from users.urls import app_name
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('expenses/', views.Expenses.as_view(), name='expense'),
    path('expenses/<int:pk>/', views.Expenses.as_view(), name='edit_expense'),
    path('expenses/create/', views.Expenses.as_view(), name='create_expense'),
    path('dict/', views.dictionary, name='dict'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category_edit'),
    path('export/csv/', views.FileExportImport().templatecsv, name='export_csv'),
    path('upload/csv/', views.FileExportImport().readcsv, name='upload_csv'),
]