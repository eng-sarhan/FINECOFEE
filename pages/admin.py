from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def profile(request):
    return render(request, 'accounts/profile.html')


def signin(request):
    return render(request, 'accounts/signin.html')


def signup(request):
    return render(request, 'accounts/signup.html')