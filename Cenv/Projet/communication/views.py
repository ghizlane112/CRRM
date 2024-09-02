from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from lead.models import Lead
from .models import Document
from .forms import DocumentForm
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





@login_required
def upload_document(request, pk):  # Utilisation de 'pk'
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.lead = lead
            document.uploaded_by = request.user
            document.save()
            form.save_m2m()  # Sauvegarder les relations ManyToMany (utilisateurs partagés)
            return redirect('lead_detail', pk=lead.pk)  # Utilisation de 'pk' pour correspondre
    else:
        form = DocumentForm()
    
    return render(request, 'communication/upload_document.html', {'form': form, 'lead': lead})