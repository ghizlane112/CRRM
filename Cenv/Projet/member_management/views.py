from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import MemberCreationForm
from users.models import Users

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde le membre avec les attributs choisis
            return redirect('member_list')  # Redirige vers la liste des membres
    else:
        form = MemberCreationForm()

    return render(request, 'member_management/add_member.html', {'form': form})

@user_passes_test(is_admin)
def member_list(request):
    members = Users.objects.all()  # Récupère tous les membres
    return render(request, 'member_management/member_list.html', {'members': members})