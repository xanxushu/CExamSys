from django.urls import path
from . import views

app_name = 'question_management'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('add/', views.question_add, name='question_add'),
    path('edit/<int:pk>/', views.question_edit, name='question_edit'),
    path('delete/<int:pk>/', views.question_delete, name='question_delete'),
    path('detail/<int:pk>/', views.question_detail, name='question_detail'),
]
