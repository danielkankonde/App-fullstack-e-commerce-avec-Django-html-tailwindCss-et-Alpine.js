from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Produit
from .models import Panier, LignePanier

# Afficher le panier
@login_required(login_url='login')
def cart_view(request):
    panier, created = Panier.objects.get_or_create(user=request.user)
    return render(request, 'panier/cart.html', {
        'panier': panier
    })


# Ajouter au panier
@login_required(login_url='login')
def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier, _ = Panier.objects.get_or_create(user=request.user)

    ligne, created = LignePanier.objects.get_or_create(
        panier=panier,
        produit=produit
    )

    if not created:
        ligne.quantite += 1
    ligne.save()

    # rester sur la même page
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Diminuer quantité 
@login_required(login_url='login')
def decrease_quantity(request, ligne_id):
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id,
        panier__user=request.user
    )

    ligne.quantite -= 1
    if ligne.quantite <= 0:
        ligne.delete()
    else:
        ligne.save()

    return redirect('cart')


# Augmenter quantité
@login_required(login_url='login')
def increase_quantity(request, ligne_id):
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id,
        panier__user=request.user
    )

    ligne.quantite += 1
    ligne.save()
    return redirect('cart')


# Supprimer un produit du panier
@login_required(login_url='login')
def remove_item(request, ligne_id):
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id,
        panier__user=request.user
    )
    ligne.delete()
    return redirect('cart')
