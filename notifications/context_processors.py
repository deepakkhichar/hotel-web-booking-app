from notifications.models import Notification


def notifications_processor(request):
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return {'unread_notifications_count': unread_notifications_count}
