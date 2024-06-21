from django.shortcuts import render

def home(request):
    return render(request, 'nouser/home.html')