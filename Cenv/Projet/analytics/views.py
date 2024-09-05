from django.shortcuts import render

# Create your views here.
# analyse/views.py
from django.http import JsonResponse
from lead.models import Lead
from django.db.models import Count
from campaigns.models import CompanyPublicitaire
from django.db.models import Count, Q


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
        # Leads associés à cette campagne
        leads = campaign.leads.all()
        total_leads = leads.count()
        # Leads convertis (statut "Converti")
        conversions = leads.filter(statut='Converti').count()
        # Calculer le taux de conversion (éviter la division par zéro)
        conversion_rate = (conversions / total_leads * 100) if total_leads > 0 else 0

        # Ajouter les données pour chaque campagne
        data.append({
            'campaign': campaign.name,
            'leads': total_leads,
            'conversions': conversions,
            'conversion_rate': f"{conversion_rate:.2f}%"
        })

    return JsonResponse(data, safe=False)





def dashboard_view(request):
    total_leads = Lead.objects.count()
    total_conversions = Lead.objects.filter(statut='Converti').count()  # Ajuster selon le champ de statut de conversion
    total_campaigns = CompanyPublicitaire.objects.count()

    context = {
        'total_leads': total_leads,
        'total_conversions': total_conversions,
        'total_campaigns': total_campaigns,
    }
    
    return render(request, 'parts/state.html', context)
