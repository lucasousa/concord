from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from rooms.models import Message, Room
from .forms import ProfileForm
from .models import User


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("core:home"))

    return HttpResponseRedirect(reverse("core:login"))


@login_required
def home(request):
    return render(
        request,
        "core/home.html",
        {"members": User.objects.filter(is_active=True)},
    )


@login_required
def profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso !")

        else:
            messages.error(request, "Esse username já existe.")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def chat(request, uuid):
    room = get_object_or_404(Room, uuid=uuid, user=request.user)
    messages_chat = Message.objects.filter(room=room).order_by("created_at")

    context = {
        "messages_chat": messages_chat,
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


@login_required
def users_without_rooms(request, room):
    ALL_USERS=0
    if room == ALL_USERS: 
        without_rooms=User.objects.all().exclude(id=request.user.id)
    else:
        room = get_object_or_404(Room, id=room)
        users_ids = [ user.id for user in room.user.all()]
        without_rooms=User.objects.all().exclude(id__in=users_ids, id=request.user.id)

    response = []
    for user in without_rooms:
        response.append(
            {
                "name":user.name,
                "username":user.username,
                "id":user.id
            }
        )

    return JsonResponse({"users": response}, safe=False)

