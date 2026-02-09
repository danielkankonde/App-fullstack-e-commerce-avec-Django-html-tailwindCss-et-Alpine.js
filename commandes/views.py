from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from panier.models import Panier
from .models import Commande, LigneCommande
from .forms import AdresseForm
from paiements.utils import init_paiement   # on va le créer proprement

@login_required
def checkout(request):
    panier = Panier.objects.get(user=request.user)

    if panier.lignepanier_set.count() == 0:
        return redirect('cart')

    if request.method == "POST":
        form = AdresseForm(request.POST)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.user = request.user
            adresse.save()

            # Création de la commande
            commande = Commande.objects.create(
                user=request.user,
                adresse=adresse,
                prix_total=panier.total_price(),
                statut="En attente"
            )

            # Copier les lignes du panier vers la commande
            for ligne in panier.lignepanier_set.all():
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne.produit,
                    quantite=ligne.quantite,
                    prix_unitaire=ligne.produit.prix
                )

            # Lancer le paiement
            return redirect(init_paiement(request, commande, "mobilemoney"))

    else:
        form = AdresseForm()

    return render(request, "commandes/commande.html", {
        "panier": panier,
        "form": form
    })
