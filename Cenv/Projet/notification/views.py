# notification/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from .forms import ReminderForm
from Rendez.models import Event
from django.views.decorators.http import require_POST

@login_required
def notifications(request):
    if request.method == 'POST':
        # Marquer les notifications comme lues
        notification_ids = request.POST.getlist('notification_ids[]')
        Notification.objects.filter(id__in=notification_ids, recipient=request.user).update(is_read=True)
        return JsonResponse({'status': 'success'})

    # GET request handling
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Compte les notifications non lues
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourne les données en JSON pour les appels AJAX
        notifications_data = list(notifications.values('id', 'sender', 'message', 'created_at', 'is_read'))
        return JsonResponse({'unread_count': unread_count, 'notifications': notifications_data})

    return render(request, 'notification/notifications.html', {'notifications': notifications, 'unread_count': unread_count})

@login_required
def create_reminder(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    else:
        event = None
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.event = event
            reminder.save()
            return redirect('notifications')
    else:
        form = ReminderForm()
    return render(request, 'notification/create_reminder.html', {'form': form, 'event': event})






@require_POST
def mark_notifications_as_read(request):
    notification_ids = request.POST.getlist('notification_ids[]')
    Notification.objects.filter(id__in=notification_ids, recipient=request.user).update(is_read=True)
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'status': 'success', 'unread_count': unread_count})
