from django.contrib import messages
from django.shortcuts import redirect

def custom_login_required_with_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('userLogin')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper