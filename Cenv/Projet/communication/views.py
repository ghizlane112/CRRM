from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

from .forms import MessageForm
from lead.models import Lead

from notification.models import Notification  # Importer le modèle Notification
from django.contrib.auth import get_user_model
from django.db.models import Q



@login_required
def inbox(request):
    # Récupère les messages reçus par l'utilisateur connecté
    user_id = request.GET.get('user')
    if user_id:
        messages = Message.objects.filter(
            (Q(sender_id=user_id) & Q(receiver=request.user)) |
            (Q(sender=request.user) & Q(receiver_id=user_id))
        ).order_by('timestamp')
    else:
        messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
    
    # Récupère tous les utilisateurs pour la liste de contacts
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)  # Exclure l'utilisateur actuel

    return render(request, 'communication/messages.html', {'messages': messages, 'users': users})






@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            # Créez une notification
            Notification.objects.create(
                recipient=message.receiver,
                sender=request.user,
                message=f"Vous avez reçu un nouveau message de {request.user.username}: {message.content}"
            )
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'communication/messages.html', {'form': form})






