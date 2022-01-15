from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime


from rooms.models import Message, Room

from .forms import ProfileForm
from .models import User


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("core:home"))

    return HttpResponseRedirect(reverse("core:login"))


@login_required
def home(request):
    profile_form = ProfileForm(instance=request.user)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if profile_form.is_valid():
            profile_form.save()

            return HttpResponseRedirect(reverse("core:home"))

    if not request.user.is_superuser:
        groups = []
        channels = []

        if groups:
            print("aqui1")
            groups = groups.objects.filter(user=request.user)

        if channels:
            print("aqui1")
            channels = channels.objects.filter(user=request.user)

    return render(
        request,
        "core/home.html",
        {"profile_form": profile_form, "members": User.objects.filter(is_active=True)},
    )


@login_required
def profile(request):
    return render(request, "core/profile.html")


@login_required
def chat(request, uuid):
    room = get_object_or_404(Room, uuid=uuid, user=request.user)
    messages = Message.objects.filter(room=room).order_by("created_at")

    context = {
        "messages": messages,
        "room": room,
        "user": request.user,
        "members": room.user.filter(is_active=True),
    }

    return render(request, "core/home.html", context)
    

def update_lastping(request, id, status):
    user = User.objects.get(id=id)
    user.last_ping = timezone.now()
    user.status = status
    user.save()
    return JsonResponse(data={'success': True})


def get_statuses(request):
    ret = []
    User.objects.filter(
        last_ping__lte=timezone.now()-timezone.timedelta(minutes=0.5),
        status=User.STATUS_ONLINE
    ).update(status=User.STATUS_OFFLINE)
    users = User.objects.all().values_list('id', 'status', 'last_ping')
    data = {'data': list(users)}
    return JsonResponse(data=data, safe=False)
