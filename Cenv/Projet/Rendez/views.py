from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Event, History,DeletedEvent  # Ajoutez History ici
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.dateparse import parse_date, parse_time
#logger = logging.getLogger(__name__)


@login_required
def calendar_view(request):
    if request.user.is_superuser:
        events = Event.objects.filter(deleted_at__isnull=True)
    else:
        events = Event.objects.filter(user=request.user, deleted_at__isnull=True)

    context = {
        'events': events
    }
    return render(request, 'events/calendar.html', context)


@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu = request.POST.get('lieu')
        description = request.POST.get('description')

        event = Event(
            title=title,
            start_date=start_date,
            heur=heur,
            lieu=lieu,
            description=description
        )
        event.save()

        History.objects.create(
            event=event,
            action='add',
            reason='Ajout de l\'événement',
            user=request.user,
            timestamp=timezone.now()
        )

        return JsonResponse({'status': 'success'})
    







  
@login_required
@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        title = request.POST.get('title')
        start_date_str = request.POST.get('start_date')
        heur_str = request.POST.get('heur')
        lieu = request.POST.get('lieu')
        description = request.POST.get('description')

        try:
            # Convertir les chaînes de caractères en objets date et time
            start_date = parse_date(start_date_str)
            heur = parse_time(heur_str)
            
            if not start_date or not heur:
                return JsonResponse({'status': 'error', 'message': 'Date ou heure invalide'})

            event = get_object_or_404(Event, id=event_id)
            event.title = title
            event.start_date = start_date
            event.heur = heur
            event.lieu = lieu
            event.description = description
            event.save()

            History.objects.create(
                event=event,
                action='update',
                reason='Mise à jour de l\'événement',
                user=request.user,
                timestamp=timezone.now()
            )

            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Événement introuvable'})
        except (ValueError, ValidationError, IntegrityError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})





@login_required
@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        reason = request.POST.get('reason')
        
        try:
            event = Event.objects.get(id=event_id)
            
            DeletedEvent.objects.create(
                title=event.title,
                start_date=event.start_date,
                heur=event.heur,
                description=event.description,
                deletion_reason=reason
            )
            
            History.objects.create(
                event=event,
                action='delete',
                reason=reason,
                user=request.user,
                timestamp=timezone.now()
            )
            
            event.deleted_at = timezone.now()  # Marquer comme supprimé
            event.save()
            
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Événement introuvable'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})





def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required
def event_list(request):
    user = request.user
    if user.is_superuser:
        events = Event.objects.filter(deleted_at__isnull=True)
    else:
        events = Event.objects.filter(user=user, deleted_at__isnull=True)

    events_data = [{
        'id': event.id,
        'title': event.title,
        'start': f"{event.start_date}T{event.heur}",
        'description': event.description,
    } for event in events]
    
    return JsonResponse(events_data, safe=False)




def history_view(request):
    today = timezone.now().date()
    
    # Récupérer les événements passés
    past_events = Event.objects.filter(start_date__lt=today)
    
    # Récupérer les événements futurs
    future_events = Event.objects.filter(start_date__gte=today)
    
    # Préparer les données pour la table des événements passés
    past_event_data = []
    for event in past_events:
        deleted = History.objects.filter(event=event, action='delete').exists()
        past_event_data.append({
            'id': event.id,
            'title': event.title,
            'start_date': event.start_date,
            'start_time': event.heur,
            'location': event.lieu,
            'description': event.description,
            'deleted': 'Oui' if deleted else 'Non'
        })
    
    # Préparer les données pour la table des événements futurs
    future_event_data = []
    for event in future_events:
        deleted = History.objects.filter(event=event, action='delete').exists()
        future_event_data.append({
            'id': event.id,
            'title': event.title,
            'start_date': event.start_date,
            'start_time': event.heur,
            'location': event.lieu,
            'description': event.description,
            'deleted': 'Oui' if deleted else 'Non'
        })

    context = {
        'past_event_data': past_event_data,
        'future_event_data': future_event_data,
        'histories': History.objects.all()
    }
    
    return render(request, 'events/history.html', context)




#def event_detail(request, event_id):
    # Essayez de récupérer l'événement
    #event = get_object_or_404(Event, id=event_id)
    
    # Vérifiez s'il existe un historique de suppression pour cet événement
    #try:
     #   deletion_history = History.objects.get(event=event)
    #    is_deleted = True
   # except History.DoesNotExist:
      #  deletion_history = None
     #   is_deleted = False

    #context = {
      #  'event': event,
     #   'deletion_history': deletion_history,
    #    'is_deleted': is_deleted
   # }

  #  return render(request, 'events/event_detail.html', context)


  
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Récupérer tout l'historique lié à cet événement
    histories = History.objects.filter(event=event).order_by('-timestamp')

    context = {
        'event': event,
        'histories': histories,
    }

    return render(request, 'events/event_detail.html', context)


