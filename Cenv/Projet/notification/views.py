from django.shortcuts import render
# notification/views.py
from .models import Reminder, Lead
from django.shortcuts import render,redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import HttpResponseRedirect
from .models import Reminder
from .forms import ReminderForm
from django.http import JsonResponse

@login_required
def notifications(request):
    # Récupère les notifications pour l'utilisateur connecté
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Compte les notifications non lues
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourne les données en JSON pour les appels AJAX
        return JsonResponse({'unread_count': unread_count})

    return render(request, 'notification/notifications.html', {'notifications': notifications, 'unread_count': unread_count})





#@login_required
#def list_reminders(request):
#    reminders = Reminder.objects.filter(user=request.user)  # Filtre les rappels pour l'utilisateur connecté
#    return render(request, 'notification/list_reminders.html', {'reminders': reminders})





def create_reminder(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)  # Assurer que le lead existe
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder_time = form.cleaned_data['reminder_time']
            message = form.cleaned_data['note']
            # Créer une notification pour le rappel
            Notification.objects.create(
                recipient=request.user,
                sender=request.user,  # ou un autre utilisateur qui crée le rappel
                message=message,
                reminder_time=reminder_time,
            )
            return HttpResponseRedirect('/reminders/')  # Rediriger vers la liste des rappels ou ailleurs
    else:
        form = ReminderForm()
    return render(request, 'notification/create_reminder.html', {'form': form, 'lead': lead})