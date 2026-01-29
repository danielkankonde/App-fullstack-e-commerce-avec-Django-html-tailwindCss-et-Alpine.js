from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from products.models import Produit
from .models import Panier, LignePanier

# Création des views
@login_required(login_url='login')
def cart_view(request):
    return render(request, 'panier/cart.html')

@login_required(login_url='login')
def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    # Récupérer ou créer le panier de l'utilisateur
    panier, created = Panier.objects.get_or_create(user=request.user)

    # Vérifier si le produit est déjà dans le panier
    ligne_panier, created = LignePanier.objects.get_or_create(
        panier=panier,
        produit=produit
    )

    if not created:
        ligne_panier.quantite += 1
    ligne_panier.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

