from django.shortcuts import render, redirect,get_object_or_404
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 修改为登录页面的URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('id_username')
        password = request.POST.get('id_password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')  # 重定向到 dashboard
        else:
            # 可选：登录失败时的处理
            return render(request, 'login.html', {'error': '无效的用户名或密码'})

    return render(request, 'login.html')

@login_required
def edit_user(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            # 可能需要重新登录用户
            update_session_auth_hash(request, password_form.user)
            messages.success(request, '密码修改成功，请重新登录。')
            return redirect('logout')
    else:
        user_form = CustomUserChangeForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'registration/edit_user.html', {'user_form': user_form, 'password_form': password_form})