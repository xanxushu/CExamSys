from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type',)
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # 更新 user_type 字段以仅包括教师和学生
        self.fields['user_type'].choices = [
            (CustomUser.TEACHER, '任课教师'),
            (CustomUser.STUDENT, '学生')
        ]

class CustomUserChangeForm(UserChangeForm):
    password = None  # 移除密码字段，防止直接在这个表单上更改密码
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': '用户名',
            'first_name': '名',
            'last_name': '姓',
            'email': '电子邮箱',
        }