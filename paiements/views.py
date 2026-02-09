from django.shortcuts import redirect
from .models import Paiement

def paiement_callback(request):
    status = request.GET.get("status")
    tx_ref = request.GET.get("tx_ref")

    paiement = Paiement.objects.get(reference=tx_ref)
    commande = paiement.commande

    if status == "successful":
        paiement.statut = "SUCCESS"
        commande.statut = "Payée"

        # vider le panier
        panier = commande.user.panier
        panier.lignepanier_set.all().delete()

    else:
        paiement.statut = "FAILED"
        commande.statut = "Échec paiement"

    paiement.save()
    commande.save()

    return redirect("home")
