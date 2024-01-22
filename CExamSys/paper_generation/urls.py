from django.urls import path
from . import views

app_name = 'paper_generation'

urlpatterns = [
    path('', views.paper_list, name='paper_list'),
    path('add/', views.paper_add, name='paper_add'),
    path('<int:pk>/edit/', views.paper_edit, name='paper_edit'),
    path('<int:pk>/delete/', views.paper_delete, name='paper_delete'),
    path('<int:pk>/detail', views.paper_detail, name='paper_detail'),
    path('auto-generate/', views.auto_generate_paper, name='auto_generate_paper'),
]
