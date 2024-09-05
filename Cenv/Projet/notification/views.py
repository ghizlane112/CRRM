from django.shortcuts import render
# notification/views.py
from .models import Reminder, Lead
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import HttpResponseRedirect
from .models import Reminder, Event
from .forms import ReminderForm
from django.http import JsonResponse

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



#@login_required
#def list_reminders(request):
#    reminders = Reminder.objects.filter(user=request.user)  # Filtre les rappels pour l'utilisateur connecté
#    return render(request, 'notification/list_reminders.html', {'reminders': reminders})



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
            reminder.event = event  # Assurez-vous que 'event' est correctement attribué
            reminder.save()
            return redirect('notifications')
    else:
        form = ReminderForm()
    
    return render(request, 'notification/create_reminder.html', {'form': form, 'event': event})