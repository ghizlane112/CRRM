from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import Http404

from django.contrib.auth.decorators import user_passes_test
from .forms import MemberCreationForm
from users.models import Users
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
User = get_user_model()


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



@user_passes_test(is_admin)
def delete_member(request, user_id):
    try:
        member = get_object_or_404(Users, id=user_id)
        if member == request.user and not Users.objects.filter(is_superuser=True).exclude(id=member.id).exists():
            messages.error(request, "Vous ne pouvez pas supprimer le seul administrateur.")
            return redirect('member_list')
        member.delete()
        messages.success(request, "Membre supprimé avec succès.")
    except Http404:
        messages.error(request, "Utilisateur non trouvé.")
    return HttpResponseRedirect(reverse('member_list'))