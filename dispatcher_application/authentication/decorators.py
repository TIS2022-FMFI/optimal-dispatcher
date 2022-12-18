from django.http import HttpResponse
from django.shortcuts import redirect


'''
if user is authenticated then user can not access login page so decorator
redirects user to default home page(different home page for superuser and user) 
'''
def is_not_authenticated():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect('/management/create-user')
                return redirect('/transports')
            return view_func(request, *args, **kwargs)

        return wrapper_func
    return decorator