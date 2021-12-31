from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("core:home"))

    return render(request, "core/login.html")


@login_required
def home(request):
    return render(request, "core/home.html")


@login_required
def profile(request):
    return render(request, "core/profile.html")
