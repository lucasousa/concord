from django.db.models import Count, Q
from rooms.models import Room


def get_rooms(request):
    if not request.user.is_authenticated:
        return dict()
    groups = Room.objects.annotate(user__count=Count("user")).filter(
        Q(every_one_send_message=True) & ~Q(user__count=2)
    )
    channels = Room.objects.filter(every_one_send_message=False)
    one_a_one = Room.objects.annotate(user__count=Count("user")).filter(
        user__count=2, user=request.user, every_one_send_message=True
    )
    if not request.user.is_superuser:
        return {
            "groups": groups.filter(user=request.user),
            "channels": channels.filter(user=request.user),
            "one_a_one": one_a_one,
        }
    return {
        "groups": groups,
        "channels": channels,
        "one_a_one": one_a_one,
    }
