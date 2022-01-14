from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404


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
            groups = groups.objects.filter(user=request.user)

        if channels:
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
        "user":user
    }

    return render(request, "core/home.html", context)


