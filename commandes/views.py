from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from panier.models import Panier
from .models import Commande, LigneCommande
from .forms import AdresseForm
from paiements.utils import PaymentInitializationError, init_paiement


@login_required
def checkout(request):
    panier = get_object_or_404(Panier, user=request.user)

    if panier.lignepanier_set.count() == 0:
        return redirect('cart')

    if request.method == "POST":
        form = AdresseForm(request.POST)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.user = request.user
            adresse.save()

            # Création UNIQUE de la commande
            commande = Commande.objects.create(
                user=request.user,
                adresse=adresse,
                prix_total=panier.total_price(),
                statut="EN_ATTENTE"
            )

            # Création de TOUTES les lignes
            for ligne in panier.lignepanier_set.all():
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne.produit,
                    quantite=ligne.quantite,
                    prix_unitaire=ligne.produit.prix
                )

            # 👉 AFFICHAGE DU POPUP (APRÈS la boucle)
            return render(request, "commandes/commande.html", {
                "panier": panier,
                "form": form,
                "commande": commande,
                "open_payment": True
            })

    else:
        form = AdresseForm()

    return render(request, "commandes/commande.html", {
        "panier": panier,
        "form": form
    })

# Dans commandes/views.py
@login_required
def lancer_paiement(request, commande_id):

    if request.method == "POST":
        commande = get_object_or_404(Commande, id=commande_id, user=request.user)
        methode = request.POST.get("methode")

        if methode not in ["card", "mobilemoney"]:
            return JsonResponse({"error": "Methode de paiement invalide."}, status=400)

        try:
            payment_url = init_paiement(request, commande, methode)
        except PaymentInitializationError as e:
            return JsonResponse({"error": e.user_message}, status=400)

        if payment_url:
            return JsonResponse({"success": True, "payment_url": payment_url})
        else:
            # On renvoie une erreur JSON propre au lieu d'une erreur 500
            return JsonResponse({
                "error": "Le service de paiement est indisponible. Vérifiez vos clés API."
            }, status=400)
        
    return JsonResponse({"error": "Invalid request"}, status=400)
