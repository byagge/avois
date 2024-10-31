# apps/your_app/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'template/index.html')
