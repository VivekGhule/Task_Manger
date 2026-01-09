# Task_Manager\apps\tasks\presenters.py
from django.contrib.auth import authenticate
from .models import User

class AuthPresenter:

    @staticmethod
    def register(email, password):
        if User.objects.filter(email=email).exists():
            return None
        return User.objects.create_user(email=email, password=password)

    @staticmethod
    def login(email, password):
        return authenticate(email=email, password=password)
