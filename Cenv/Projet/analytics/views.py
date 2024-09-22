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
    data = Lead.objects.values('statut').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)




def lead_source_data(request):
    data = Lead.objects.values('source').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)

# analyse/views.py

def lead_conversion_data(request):
    # Exemple hypothétique, ajustez en fonction de votre modèle de données
    data = Lead.objects.values('campaign').annotate(conversions=Count('id'))
    return JsonResponse(list(data), safe=False)


def conversion_report_view(request):
    campaigns = CompanyPublicitaire.objects.all()
    data = []

    for campaign in campaigns:
        leads = campaign.leads.all()
        total_leads = leads.count()
        conversions = leads.filter(statut='Converti').count()

        print(f"Campagne: {campaign.name}, Total Leads: {total_leads}, Conversions: {conversions}")  # Log

        conversion_rate = (conversions / total_leads * 100) if total_leads > 0 else 0

        data.append({
            'campaign': campaign.name,
            'leads': total_leads,
            'conversions': conversions,
            'conversion_rate': f"{conversion_rate:.2f}%"
        })

    return JsonResponse(data, safe=False)



def dashboard_view(request):
    total_leads = Lead.objects.count()
    total_conversions = Lead.objects.filter(statut='Converti').count()
    total_campaigns = CompanyPublicitaire.objects.count()

    context = {
        'total_leads': total_leads,
        'total_conversions': total_conversions,
        'total_campaigns': total_campaigns,
        'show_stats': False  # Mettre à False pour ne pas afficher les statistiques
    }

    return render(request, 'parts/state.html', context)
