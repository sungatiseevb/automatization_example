from django.shortcuts import render
import main


def home(request):
    return render(request, 'index.html')


def documentation(request):
    return render(request, 'documentation.html')