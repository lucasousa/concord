from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone


from rooms.models import Message, Room
from .models import User
from .forms import ProfileForm

def index(request):
    if request.user.is_authenticated:        
        return HttpResponseRedirect(reverse("core:home"))

    return HttpResponseRedirect(reverse("core:login"))


@login_required
def home(request):
    profile_form = ProfileForm()
    if request.method == 'POST' or request.method == 'PATCH':
        profile = get_object_or_404(User, pk=request.user.pk)

        profile_form = ProfileForm(request.POST)
        profile_form.is_valid()
        if profile_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            profile.name = profile_form.cleaned_data['name']
            profile.username = profile_form.cleaned_data['username']
            profile.save()
            return HttpResponseRedirect(reverse('core:home'))

    groups = Room.objects.filter(every_one_send_message=True)
    channels = Room.objects.filter(every_one_send_message=False)

    if not request.user.is_superuser:
        groups = []
        channels = []

        if groups:
            print("aqui1")
            groups = groups.objects.filter(user=request.user)

        if channels:
            print("aqui1")
            channels = channels.objects.filter(user=request.user)

    return render(request, "core/home.html",{
            "groups": groups,
            "channels": channels,
            "profile_form": profile_form
        }
    )


@login_required
def profile(request):
    return render(request, "core/profile.html")
    
    
    
@login_required
def chat(request):
    user = get_object_or_404(User, pk=request.user.pk)
    group = Room.objects.filter(user=user).first()
    messages = Message.objects.filter(room=group).order_by("created_at")

    context = {
        "messages": messages,
        "group": group,
        "user": user
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
    users = User.objects.all().values_list('id', 'status', 'last_ping')
    for user in users:
        print(user)
        if user[1] == 'offline' or user[2] is None or user[2] < timezone.now() - timezone.timedelta(minutes=0.5):
            ret.append(([user[0]], 'offline', user[2]))
        else:
            ret.append(user)
    data = {'data': ret}
    return JsonResponse(data=data, safe=False)






