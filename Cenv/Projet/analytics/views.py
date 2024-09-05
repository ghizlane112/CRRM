from django.shortcuts import render

# Create your views here.
# analyse/views.py
from django.http import JsonResponse
from lead.models import Lead
from django.db.models import Count
from campaigns.models import CompanyPublicitaire



def analytics_view(request):
    return render(request, 'AnalyaseFile/analytics.html')



def lead_status_data(request):
    data = Lead.objects.values('status').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)




def lead_source_data(request):
    data = Lead.objects.values('source').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)

# analyse/views.py

def lead_conversion_data(request):
    # Exemple hypothétique, ajustez en fonction de votre modèle de données
    data = Lead.objects.values('campaign').annotate(conversions=Count('id'))
    return JsonResponse(list(data), safe=False)



#def conversion_report_view(request):
    # Code pour récupérer les données et les retourner en JSON
 #   data = [
  #      {'campaign': 'Campagne A', 'leads': 100, 'conversions': 25},
   #     {'campaign': 'Campagne B', 'leads': 150, 'conversions': 45},
        # autres données
    #]
    #return JsonResponse(data, safe=False)




def conversion_report_view(request):
    # Obtenir toutes les campagnes
    campaigns = CompanyPublicitaire.objects.all()
    data = []

    # Calculer les conversions pour chaque campagne
    for campaign in campaigns:
        leads = Lead.objects.filter(campaign=campaign.name)  # Remplacez campaign.name par le champ approprié si nécessaire
        total_leads = leads.count()
        conversions = leads.filter(statut='Converti').count()

        data.append({
            'campaign': campaign.name,
            'leads': total_leads,
            'conversions': conversions
        })

    return JsonResponse(data, safe=False)

