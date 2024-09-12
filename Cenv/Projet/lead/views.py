# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from django.views.decorators.http import require_POST
from .models import Lead, Interaction,LeadHistory
import csv
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
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
from campaigns.models import CompanyPublicitaire
from django.http import JsonResponse

# Create your views here.
def one(request):
    return render(request,'principale.html')



def two(request):
    return render(request,'parts/nav.html')

def three(request):
    return render(request,'parts/button.html')

#def dashboard(request):
 #   return render(request,'dashboard.html')



def dashboard(request):
    leads = Lead.objects.all()[:5]  # Limiter le nombre de leads affichés
    return render(request, 'dashboard.html', {
        'leads': leads
    })





def search_view(request):
    query = request.GET.get('q')
    lead_results = []
    campagne_results = []

    if query:
        # Rechercher dans le modèle Lead
        lead_results = Lead.objects.filter(
            Q(nom__icontains=query) |  # Remplacez par les champs pertinents
            Q(email__icontains=query)
        )

        # Rechercher dans le modèle Campagne
        campagne_results = CompanyPublicitaire.objects.filter(
            Q(titre__icontains=query) |  # Remplacez par les champs pertinents
            Q(description__icontains=query)
        )

    # Combinez les résultats pour les envoyer au template
    context = {
        'query': query,
        'lead_results': lead_results,
        'campagne_results': campagne_results,
    }

    return render(request, 'nav.html', context)




def four(request):
    return render(request,'parts/state.html')

def lead_list(request):
    # Filtrer les leads pour exclure les archivés
    leads = Lead.objects.filter(is_deleted=False)

    search_text = request.GET.get('search', '')
    sort_field = request.GET.get('sort', '')

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

    if sort_field:
        leads = leads.order_by(sort_field)

    paginator = Paginator(leads, 8)  # 8 leads par page
    page_number = request.GET.get('page')

    try:
        leads = paginator.get_page(page_number)
    except PageNotAnInteger:
        leads = paginator.get_page(1)
    except EmptyPage:
        leads = paginator.get_page(paginator.num_pages)

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
# Création d'un lead
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
            lead.statut = 'Nouveau'
            lead.save()
            
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












# Modification d'un lead
@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead, user=request.user)
        if form.is_valid():
            old_data = f"Nom: {lead.nom}, Prénom: {lead.prenom}, Email: {lead.email}, Téléphone: {lead.telephone}, Source: {lead.source}, Statut: {lead.statut}, Note: {lead.note}"
            lead = form.save()
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
    
    # Pagination
    paginator = Paginator(histories, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    
    try:
        histories_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        histories_page = paginator.get_page(1)
    except EmptyPage:
        histories_page = paginator.get_page(paginator.num_pages)
    
    return render(request, 'leadfile/LeadHistory.html', {'histories': histories_page})






@login_required
@require_POST
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    # Enregistrez l'action dans l'historique
    LeadHistory.objects.create(
        lead=lead,
        user=request.user,
        action='deleted',
        details=f'Lead archivé avec les informations: {lead}'
    )

    # Archiver le lead au lieu de le supprimer
    lead.is_deleted = True
    lead.deleted_at = timezone.now()
    lead.save()

    return redirect('lead_list')  # Redirige vers la liste des leads


def archive_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.is_deleted = True
    lead.deleted_at = timezone.now()
    lead.save()
    return redirect('LeadHistory')

class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer




@login_required
def add_interaction(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.user != lead.responsable and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas l'autorisation d'ajouter une interaction à ce lead.")
        return redirect('lead_detail', pk=lead.pk)
    
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead
            interaction.utilisateur = request.user
            interaction.save()
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = InteractionForm()
    
    interactions = Interaction.objects.filter(lead=lead)
    return render(request, 'leadfile/add_interaction.html', {
        'form': form,
        'lead': lead,
        'interactions': interactions
    })

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





