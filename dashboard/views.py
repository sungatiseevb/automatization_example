from django.shortcuts import render
import main


def home(request):
    return render(request, 'index.html')
