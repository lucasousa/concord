from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from rooms.models import Room

def index(request):
    if request.user.is_authenticated:        
        return HttpResponseRedirect(reverse("core:home"))

    return HttpResponseRedirect(reverse("core:login"))


@login_required
def home(request):

    groups = Room.objects.filter(every_one_send_message=True)
    channels = Room.objects.filter(every_one_send_message=False)

    if not request.user.is_superuser:
        groups = groups.objects.filter(user=request.user) 
        channels = channels.objects.filter(user=request.user)

    return render(request, "core/home.html",{
            "groups":groups, 
            "channels":channels
        }
    )


@login_required
def profile(request):
    return render(request, "core/profile.html")


