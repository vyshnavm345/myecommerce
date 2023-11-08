from django.shortcuts import render, redirect
from .models import ReferenceProfile

# Create your views here.
def main_view(request, *args, **kwargs):
    
    code = str(kwargs.get('ref_code'))
    try:
        profile = ReferenceProfile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id',profile.id)
    except:
        pass
        print(request.session.get_expiry_age())
        
    return redirect("userSignup")


def customer_referals(request):
    my_profile = ReferenceProfile.objects.get(user= request.user)
    my_referals = my_profile.get_recommended_profiles()
    referal_code = my_profile.get_referal_link()
    context = {
        "my_referals" : my_referals,
        "referal_code" : referal_code,
    }
    return render(request, 'referals/customer_referals.html', context)