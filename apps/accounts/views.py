from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import RegistrationForm, LoginForm, PasswordResetForm

User = get_user_model()

def register_view(request):
    # Проверка: если пользователь уже вошел в систему, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('homepage')  # Замените 'homepage' на нужный URL

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Сохраняем пароль хэшированным
            user.save()
            login(request, user)  # Авторизуем пользователя после регистрации
            return redirect('homepage')  # Замените 'homepage' на нужный URL
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    # Проверка: если пользователь уже вошел в систему, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('homepage')  # Замените 'homepage' на нужный URL

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('homepage')  # Замените 'homepage' на нужный URL

    return render(request, 'accounts/login.html', {'form': form})

def reset_password_view(request):
    # Проверка: если пользователь уже вошел в систему, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('homepage')  # Замените 'homepage' на нужный URL

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправляем на страницу входа после сброса пароля
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/reset_password.html', {'form': form})
