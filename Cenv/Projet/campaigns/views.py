from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import CampaignForm
# Create your views here.
from .models import CompanyPublicitaire

def campaign_list(request):
    campaigns = CompanyPublicitaire.objects.all()
    context = {
        'campaigns': campaigns,
    }
    return render(request, 'campaigns/campaign_list.html', context)



def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')  # Redirige vers la liste des campagnes après ajout
    else:
        form = CampaignForm()
    
    return render(request, 'campaigns/add_campaign.html', {'form': form})
