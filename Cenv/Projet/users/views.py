from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def permission(request):
   user = request.user
    
    #Vérifier si l'utilisateur est dans le groupe "Administrateurs"
   is_admin = user.groups.filter(name='administrateurs').exists()
    
    # Vérifier si l'utilisateur est dans le groupe "Membres"
   is_member = user.groups.filter(name='utilisateurs').exists()
    
    # Préparer le contexte en fonction des groupes
   context = {
       'is_admin': is_admin,
       'is_member': is_member,
        # Ajouter d'autres contextes ici si nécessaire
    }
    
   return render(request, 'parts/button.html', context)