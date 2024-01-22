from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_management'
    # 添加下面这行来定义应用的模板目录
    path = 'user_management'