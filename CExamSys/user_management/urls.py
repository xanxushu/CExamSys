from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('edit/', views.edit_user, name='edit_user'),
    # 其他URL配置...
]
