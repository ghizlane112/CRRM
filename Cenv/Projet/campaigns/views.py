from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import CampaignForm
# Create your views here.
from lead.models import Lead 
from .models import CompanyPublicitaire


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
            campaign = form.save()  # Sauvegarde la campagne et les relations Many-to-Many
            return redirect('campaign_list')
    else:
        form = CampaignForm()

    context = {
        'form': form,
    }
    return render(request, 'campaigns/add_campaign.html', context)
