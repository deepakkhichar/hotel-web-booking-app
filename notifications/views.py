from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from notifications.models import Notification


@login_required
def notification_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of notifications for the current user.

    This function retrieves all notifications for the current user and
    displays them in a list, ordered by creation date (newest first).

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered notification list page
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def mark_as_read(request: HttpRequest, notification_id: int) -> HttpResponse:
    """
    Mark a specific notification as read.

    This function updates a notification's status to 'read' and redirects
    the user back to the notification list.

    Args:
        request (HttpRequest): The incoming HTTP request
        notification_id (int): The ID of the notification to mark as read

    Returns:
        HttpResponse: Redirect to notification list
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')


@login_required
def mark_all_as_read(request: HttpRequest) -> HttpResponse:
    """
    Mark all notifications for the current user as read.

    This function updates all unread notifications for the current user
    to 'read' status and redirects the user back to the notification list.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Redirect to notification list with success message
    """
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')
