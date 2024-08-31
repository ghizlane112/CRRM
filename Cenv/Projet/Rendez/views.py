from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Event, History  # Ajoutez History ici
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#logger = logging.getLogger(__name__)

def calendar_view(request):
    if request.method == 'GET':
        # Renvoie la page HTML du calendrier
        return render(request, 'events/calendar.html')
   

@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu=request.POST.get('lieu')
        description = request.POST.get('description')

        event = Event(
            title=title,
            start_date=start_date,
            heur=heur,
            lieu=lieu,
            description=description
        )
        event.save()
        return JsonResponse({'status': 'success'})
       
    








@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu=request.POST.get('lieu')
        description = request.POST.get('description')

        event = get_object_or_404(Event, id=event_id)
        event.title = title
        event.start_date = start_date
        event.heur = heur
        event.lieu=lieu
        event.description = description
        event.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide'})






@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        reason = request.POST.get('reason', '')  # Obtenez la raison de la suppression
        event = get_object_or_404(Event, id=event_id)
        
        # Créez un enregistrement dans le modèle History avant de supprimer l'événement
        History.objects.create(
            event=event,
            action='delete',
            reason=reason,
           # user=request.user  # Enregistrez l'utilisateur connecté
        )
        
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide'})






def dashboard_view(request):
    return render(request, 'dashboard.html')



def event_list(request):
    # Renvoie les événements en JSON pour FullCalendar
    events = Event.objects.all()
    events_data = [{
        'id': event.id,
        'title': event.title,
        'start': f"{event.start_date}T{event.heur}",  # Combine la date et l'heure pour FullCalendar
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




def event_detail(request, event_id):
    # Essayez de récupérer l'événement
    event = get_object_or_404(Event, id=event_id)
    
    # Vérifiez s'il existe un historique de suppression pour cet événement
    try:
        deletion_history = History.objects.get(event=event)
        is_deleted = True
    except History.DoesNotExist:
        deletion_history = None
        is_deleted = False

    context = {
        'event': event,
        'deletion_history': deletion_history,
        'is_deleted': is_deleted
    }

    return render(request, 'events/event_detail.html', context)