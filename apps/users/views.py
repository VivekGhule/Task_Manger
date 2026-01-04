# Task_Manager\apps\tasks\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .presenters import AuthPresenter

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AuthPresenter.register(email, password)
        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'auth/register.html', {'error': 'Email already exists'})

    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AuthPresenter.login(email, password)
        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
