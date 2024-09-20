
from django.http import HttpResponse
import openpyxl
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from .forms import CampaignForm
from lead.models import Lead 
from .models import CompanyPublicitaire
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import CompanyPublicitaire
import io



def campaign_list(request):
    campaigns = CompanyPublicitaire.objects.prefetch_related('leads').all()
    context = {
        'campaigns': campaigns,
    }
    return render(request, 'campaigns/campaign_list.html', context)





def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()

    context = {
        'form': form,
    }
    return render(request, 'campaigns/add_campaign.html', context)

def export_campaigns(request):
    # Créer un classeur Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Campagnes"

    # Ajouter des en-têtes
    ws.append(["Nom de la Campagne", "Date de Début", "Date de Fin", "Budget", "Nom de l'Entreprise", "Leads"])

    # Ajouter des données
    for campaign in CompanyPublicitaire.objects.prefetch_related('leads').all():
        leads = ', '.join([f"{lead.prenom} {lead.nom}" for lead in campaign.leads.all()])
        ws.append([
            campaign.name,
            campaign.start_date.strftime('%Y-%m-%d'),
            campaign.end_date.strftime('%Y-%m-%d'),
            campaign.budget or '',
            campaign.nom_entreprise or 'Non spécifié',
            leads
        ])

    # Préparer la réponse HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="campagnes.xlsx"'

    # Écrire le classeur Excel dans la réponse
    wb.save(response)
    return response






def export_campaigns_pdf(request):
    # Créer une réponse HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="campagnes.pdf"'

    # Créer un tampon pour stocker le PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Ajouter un titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Liste des Campagnes")

    # Définir la police pour le contenu
    p.setFont("Helvetica", 12)

    y = height - 80

    # Ajouter les en-têtes
    headers = ["Nom de la Campagne", "Date de Début", "Date de Fin", "Budget", "Nom de l'Entreprise", "Leads"]
    x_positions = [100, 200, 300, 400, 500, 600]
    for x, header in zip(x_positions, headers):
        p.drawString(x, y, header)
    y -= 20

    # Ajouter les données des campagnes
    campaigns = CompanyPublicitaire.objects.prefetch_related('leads').all()
    for campaign in campaigns:
        leads = ', '.join([f"{lead.prenom} {lead.nom}" for lead in campaign.leads.all()])
        line = [
            campaign.name,
            campaign.start_date.strftime('%Y-%m-%d'),
            campaign.end_date.strftime('%Y-%m-%d'),
            str(campaign.budget or ''),
            campaign.nom_entreprise or 'Non spécifié',
            leads
        ]
        for x, value in zip(x_positions, line):
            p.drawString(x, y, value)
        y -= 20

        # Ajouter une nouvelle page si nécessaire
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    # Envoyer le PDF dans la réponse HTTP
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()
    return response



def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(CompanyPublicitaire, id=campaign_id)
    all_leads = Lead.objects.filter(is_deleted=False)  # Récupérer tous les leads

    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        new_lead_id = request.POST.get('new_lead')  # Récupérer le nouvel ID de lead
        if form.is_valid():
            form.save()  # Sauvegarder les modifications de la campagne
            
            # Ajouter le nouvel lead s'il est sélectionné et n'est pas déjà présent
            if new_lead_id:
                lead = Lead.objects.get(id=new_lead_id)
                if lead not in campaign.leads.all():  # Vérifier si le lead est déjà associé
                    campaign.leads.add(lead)  # Ajouter le nouveau lead

            return HttpResponseRedirect('/campaigns/')  # Rediriger vers la liste des campagnes
    else:
        form = CampaignForm(instance=campaign)

    context = {
        'form': form,
        'all_leads': all_leads,  # Passer tous les leads au contexte
        'campaign': campaign,  # Passer la campagne pour afficher le nom
    }
    return render(request, 'campaigns/edit_campaign.html', context)
