from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Room
from core.models import User


def room(request):
    if request.method == "POST":
        datas = request.POST

        if datas.get('room', False):
            room = Room.objects.get(id=datas["room"])
            room.name = datas["name"]
            room.type = datas["type"]

            if datas.get("every_one_send_message", False):
                room.every_one_send_message = True
            else:
                room.every_one_send_message = False

            users = User.objects.filter(id__in=datas["users_list"].split(","))
            room.user.clear()
            room.user.add(*users)
            room.save()

        else:
            new_room = Room.objects.create(name=datas["name"], type=datas["type"])
            if not datas.get("every_one_send_message", False):
                new_room.every_one_send_message = False

            users = User.objects.filter(username__in=datas["users"].split(","))
            new_room.user.add(*users)
            new_room.save()

        return HttpResponseRedirect(reverse("core:home"))


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

        room.user.remove(user)
        
        return HttpResponseRedirect(reverse("core:home"))


