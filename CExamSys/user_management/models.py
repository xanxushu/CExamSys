from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 用户类型常量
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3

    USER_TYPE_CHOICES = (
        (ADMIN, '管理员'),
        (TEACHER, '任课教师'),
        (STUDENT, '学生'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=STUDENT)
