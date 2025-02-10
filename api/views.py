from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView as BaseLoginView
from .serializers import LoginSerializer

# Create your views here.

class RegisterView(BaseRegisterView):
    def create(self, request, *args, **kwargs):
        # Rename the password fields in the request data
        data = request.data.copy()
        if 'password' in data:
            data['password1'] = data.pop('password')
        if 'confirm_password' in data:
            data['password2'] = data.pop('confirm_password')
        request._full_data = data
        return super().create(request, *args, **kwargs)

class LoginView(BaseLoginView):
    serializer_class = LoginSerializer
