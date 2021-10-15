from django.shortcuts import render

from .models import Profile
from .forms import ProfileForm

from django.contrib.auth.decorators import login_required




@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confrim = False

    if form.is_valid():
        form.save()
        confrim = True
    
    context = {
        'profile': profile,
        'form':form,
        'confrim':confrim
    }
    return render(request, 'profiles/main.html', context)
    