from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.views.generic import View

class UserCreationForm(View):
    template = 'user_management/user_creation.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)

    def post(self, request):
        ...


