import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .models import Room
from core.models import User


def room(request):
    if request.method == "POST":
        datas = request.POST

        if datas.get('room', False):
            room = Room.objects.get(id=datas["room"])
            room.name = datas["name"]

            if datas.get("every_one_send_message", False):
                room.every_one_send_message = True
            else:
                room.every_one_send_message = False
            
            users_ids = datas["users_list"].split(",") or []
            users_ids.append(request.user.id)
            users_ids = [int(x) for x in users_ids]
            users_ids.sort()
            
            if not check_create(users_ids):
                room.delete()

            else:
                users = User.objects.filter(id__in=users_ids)
                room.user.clear()
                room.user.add(*users)
                room.save()

        else:
            users_ids = request.POST.getlist('usersNewRoom')
            users_ids.append(request.user.id)
            users_ids = [int(x) for x in users_ids]
            users_ids.sort()

            if not check_create(users_ids):
                return HttpResponseRedirect(reverse("core:home"))

            new_room = Room.objects.create(name=datas["name"])

            if not datas.get("every_one_send_message", False):
                new_room.every_one_send_message = False
    
            users = User.objects.filter(id__in=users_ids)
            new_room.user.add(*users)
            new_room.save()

        return HttpResponseRedirect(reverse("core:home"))

def check_create(users_ids):
    rooms = Room.objects.annotate(qtd_user=Count("user")).filter(
                qtd_user=2
            )

    if len(users_ids)==2:
        for room in rooms:
            if list(room.user.all().order_by("id").values_list("id", flat=True)) == users_ids:
                return False
    return True

def room_delete(request):
    if request.method == "POST":
        datas = request.POST
        Room.objects.filter(
            id=datas["room_id_delete"]
        ).delete()

        return HttpResponseRedirect(reverse("core:home"))


def room_remove_participant(request):
    if request.method == "POST":
            
        datas = request.POST
        room = Room.objects.get(id=datas["id_room"])
        user = User.objects.get(id=datas["id_participant"])
        users_ids = list(room.user.all().exclude(id=user.id).order_by("id").values_list("id", flat=True))
        room.user.remove(user)
       
        if not check_create(users_ids):
           room.delete()
        
        return HttpResponseRedirect(reverse("core:home"))


@login_required
def add_new_members(request):
    datas = json.loads(request.body.decode("utf-8"))

    room = Room.objects.get(id=datas["room"])
    users = User.objects.filter(id__in=datas["users"])
    
    users_ids = list(room.user.all().order_by("id").values_list("id", flat=True))
    users_ids += list(users.values_list("id", flat=True))
    users_ids.sort()

    if not check_create(users_ids):
        room.delete()
        return JsonResponse({}, status=301, safe=False)
    else:
        room.user.add(*users)

    return JsonResponse({"status": "ok"}, safe=False)

