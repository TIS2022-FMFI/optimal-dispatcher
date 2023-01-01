from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

# decorators
from .decorators import is_not_authenticated
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class LoginView(View):
    template = 'authentication/login.html'

    @method_decorator(is_not_authenticated())
    def get(self, request):
        context = {}
        return render(request, self.template, context)


    @method_decorator(is_not_authenticated())
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('user-list')
            return redirect('transportation-list')

        context = {'email' : email, 'error_message' : 'Wrong email or password'}
        return render(request, self.template, context)

