# apps/notifications/views.py

from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})
