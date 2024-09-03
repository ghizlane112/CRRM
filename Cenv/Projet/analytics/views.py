from django.shortcuts import render

# Create your views here.
# analyse/views.py
from django.http import JsonResponse
from lead.models import Lead
from django.db.models import Count



def analytics_view(request):
    return render(request, 'analytics.html')



def lead_status_data(request):
    data = Lead.objects.values('status').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)
