# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from .models import Lead, Interaction,LeadHistory
import csv
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import InteractionForm
from django.views.generic import ListView
from .forms import LeadSortForm
from .forms import LeadForm, NoteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import LeadSerializer
from django.db.models import Q

# Create your views here.
def one(request):
    return render(request,'principale.html')



def two(request):
    return render(request,'parts/nav.html')

def three(request):
    return render(request,'parts/button.html')

#def dashboard(request):
 #   return render(request,'dashboard.html')


#def lead_list_view(request):
   # leads = Lead.objects.all()  # Vous pouvez ajouter des filtres et de la pagination ici
   # return render(request, 'parts/lead_list_partial.html', {'leads': leads})



def dashboard(request):
    leads = Lead.objects.all()[:5]  # Limiter le nombre de leads affichés
    return render(request, 'dashboard.html', {
        'leads': leads
    })


def four(request):
    return render(request,'parts/state.html')


def lead_list(request):
    leads = Lead.objects.all()

    #return render(request, 'leadfile/lead_list.html', {'leads': leads})
    search_text = request.GET.get('search', '')
    sort_field = request.GET.get('sort', '')


    # Appliquer les filtres si le texte de recherche est présent
    if search_text:
        leads = leads.filter(
            Q(nom__icontains=search_text) |
            Q(prenom__icontains=search_text) |
            Q(email__icontains=search_text) |
            Q(telephone__icontains=search_text) |
            Q(source__icontains=search_text) |
            Q(statut__icontains=search_text) |
            Q(note__icontains=search_text)
        )


     # Appliquer le tri si un champ de tri est sélectionné
    if sort_field:
        leads = leads.order_by(sort_field)
    # Rendre les options de filtre disponibles pour le template

    # Pagination
    paginator = Paginator(leads, 8)  # 5 leads par page
    page_number = request.GET.get('page')  # Utiliser 1 comme page par défaut

    try:
        leads = paginator.get_page(page_number)
    except PageNotAnInteger:
        leads = paginator.get_page(1)  # Page 1 si la page demandée n'est pas un entier
    except EmptyPage:
        leads = paginator.get_page(paginator.num_pages)  # Dernière page si la page demandée est vide



    return render(request, 'leadfile/lead_list.html', {
        'leads': leads,
        'search_text': search_text,
        'sort_field': sort_field
    })









#### pour details
def lead_detail(request, pk):
    lead = Lead.objects.get(pk=pk)
    return render(request, 'leadfile/lead_detail.html', {'lead': lead})




# Optionnel: ajouter une vue pour la création si vous avez besoin de suivre les créations
@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST, user=request.user)
        if form.is_valid():
            lead = form.save(commit=False)
            if request.user.is_superuser:
                lead.responsable = form.cleaned_data['responsable']
            else:
                lead.responsable = request.user
            lead.save()
            
            # Enregistrer l'historique
            LeadHistory.objects.create(
                lead=lead,
                user=request.user,
                action='created',
                details=f'Lead créé avec les informations: {lead}'
            )
            return redirect('lead_list')
    else:
        form = LeadForm(user=request.user)
    
    return render(request, 'leadfile/lead_form.html', {'form': form})







def lead_import(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            # Handle error
            return redirect('lead_list')
        
        # Read and process CSV file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        for row in reader:
            Lead.objects.create(
                nom=row['Nom'],
                prenom=row['Prénom'],
                email=row['Email'],
                telephone=row['Téléphone'],
                source=row['Source'],
                statut=row['Statut'],
                note=row.get('Note', '')
            )
        return redirect('lead_list')

    return render(request, 'leadfile/import_leads.html')














@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead, user=request.user)
        if form.is_valid():
            old_data = f"Nom: {lead.nom}, Prénom: {lead.prenom}, Email: {lead.email}, Téléphone: {lead.telephone}, Source: {lead.source}, Statut: {lead.statut}, Note: {lead.note}"
            lead = form.save()  # Mettez à jour l'instance du lead
            new_data = f"Nom: {lead.nom}, Prénom: {lead.prenom}, Email: {lead.email}, Téléphone: {lead.telephone}, Source: {lead.source}, Statut: {lead.statut}, Note: {lead.note}"
            LeadHistory.objects.create(
                lead=lead,
                user=request.user,
                action='updated',
                details=f"Modifié de {old_data} à {new_data}"
            )
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead, user=request.user)
    return render(request, 'leadfile/lead_edit.html', {'form': form})





def lead_history(request):
    histories = LeadHistory.objects.all().order_by('-timestamp')
    return render(request, 'leadfile/LeadHistory.html', {'histories': histories})
#def lead_history(request, pk):
 #   lead = get_object_or_404(Lead, pk=pk)
  #  histories = LeadHistory.objects.filter(lead=lead).order_by('-timestamp')
   # return render(request, 'leadfile/lead_history.html', {'lead': lead, 'histories': histories})

@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
       

        # Créer une entrée dans LeadHistory avec l'utilisateur actuel
        if request.user:  # Assurez-vous que l'utilisateur est bien défini
            LeadHistory.objects.create(
                lead=lead,
                user=request.user,  # L'utilisateur connecté
                action='deleted',
                timestamp=timezone.now(),
                details=f"Lead {lead.id} supprimé"
            )
             # Supprimer le lead
        lead.delete()

        return redirect('lead_list')  # Redirection après suppression
    return render(request, 'leadfile/lead_confirm_delete.html', {'lead': lead})




class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer




def interaction_list(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interactions = lead.interactions.all()
    return render(request, 'lead/interaction_list.html', {'lead': lead, 'interactions': interactions})

def add_interaction(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead
            interaction.utilisateur = request.user
            interaction.save()
            return redirect('interaction_list', lead_id=lead.id)
    else:
        form = InteractionForm()
    return render(request, 'lead/add_interaction.html', {'form': form, 'lead': lead})




def add_note(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = lead
            note.user = request.user  # Associe la note à l'utilisateur actuel
            note.save()
            return redirect('lead_detail', pk=pk)  # Redirige vers les détails du lead
    else:
        form = NoteForm()  # Formulaire vide pour GET ou après une soumission réussie
    
    # Récupère les notes associées au lead pour l'affichage
    notes = lead.notes.all()
    
    return render(request, 'leadfile/ajouter-note.html', {
        'lead': lead,
        'notes': notes,
        'form': form
    })
