from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import logout as _logout
from django.contrib.auth import get_user_model
from django.contrib.auth import login as _login

from .forms import *

User = get_user_model()


def home(request):
    return HttpResponse("Home Sweet Home :)")


def login(request):
    if request.method == 'GET':
        form = CustomAuthenticationForm(request)
        return render(request, 'app/login.html', {'form': form})
    elif request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['username'])
            _login(request, user)
            return redirect('/')
        return render(request, 'app/login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'app/register.html', {'form': form})
    elif request.method == 'POST':
        data = request.POST
        if data.get('is_superuser'):
            print('Is Super-User.')
        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            _login(request, user)
            return redirect('/')
        return render(request, 'app/register.html', {'form': form})


"""
form = PasswordChangeForm(request.user) # OldPassword - NewPassword - NewPasswordConfirm

form = PasswordResetForm() # Email > Reset Link

form = SetPasswordForm(request.user) # NewPassword - NewPasswordConfirm

form = AdminPasswordChangeForm(request.user) # Password - Password (again)
"""


def logout(request):
    _logout(request)
    return redirect('/')