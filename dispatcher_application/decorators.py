from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib.auth import REDIRECT_FIELD_NAME


'''
if user is authenticated then user can not access login page so decorator
redirects user to default home page(different home page for superuser and user) 
'''
def is_not_authenticated():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect('user-list')
                return redirect('transportation-list')
            return view_func(request, *args, **kwargs)

        return wrapper_func
    return decorator


'''
if user is authenticated and does not have admin rights, user is redirected back to trasport page
if user have admin rights user is redirected to the desired page
'''
def admin_permission():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            return redirect('page-not-found')
        return wrapper_func
    return decorator