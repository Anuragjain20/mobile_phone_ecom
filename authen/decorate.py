from .models import Profile
from django.shortcuts import redirect


#decorator for checking if the form is filled or not
def check_form_filled(func):
    def wrap(request, *args, **kwargs):


        profile = Profile.objects.filter(user=request.user)
       

        if  profile:
            return func(request, *args, **kwargs)
           
                
        else:
            return redirect('/accounts/profile/')

    return wrap