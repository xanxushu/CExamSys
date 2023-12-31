from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 修改为登录页面的URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
