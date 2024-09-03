from django.shortcuts import render

# Create your views here.
# analyse/views.py
from django.http import JsonResponse
from lead.models import Lead
from django.db.models import Count



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
