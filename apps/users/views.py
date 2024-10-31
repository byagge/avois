# apps/users/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from .forms import UserRegistrationForm, UserProfileForm
from apps.dynamic_content.utils import weather

# Регистрация
class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    bio = user_profile.bio
    date_joined = user_profile.date_joined

    temperature = round(weather())  # Получаем только температуру

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'bio': bio,
        'date_joined': date_joined,
        'temperature': temperature,
    })



@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'settings.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")
    return redirect('homepage')