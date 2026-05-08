import uuid

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from commandes.models import Commande
from panier.models import Panier
from .models import Paiement


def paiement_callback(request):
    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")
    flutterwave_status = request.GET.get("status")

    paiement = get_object_or_404(Paiement, reference=tx_ref)

    if flutterwave_status != "successful" or not transaction_id:
        paiement.statut = "ECHEC"
        paiement.save()
        return redirect("paiements:failed")

    try:
        response = requests.get(
            f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
            headers={"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"},
            timeout=10,
        )
        data = response.json().get("data", {})
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Erreur verification Flutterwave : {e}")
        paiement.statut = "ECHEC"
        paiement.save()
        return redirect("paiements:failed")

    if data.get("status") == "successful":
        paiement.statut = "PAYE"
        paiement.save()

        commande = paiement.commande
        commande.statut = "PAYEE"
        commande.save()

        panier, _ = Panier.objects.get_or_create(user=paiement.user)
        panier.lignepanier_set.all().delete()

        return redirect("paiements:success")

    paiement.statut = "ECHEC"
    paiement.save()
    return redirect("paiements:failed")


def payer(request, commande_id, methode):
    commande = get_object_or_404(Commande, id=commande_id)

    Paiement.objects.create(
        user=request.user,
        commande=commande,
        methode=methode,
        montant=commande.prix_total,
        reference=str(uuid.uuid4()),
        statut="INITIE",
    )

    # Pour test manuel seulement : le vrai flux passe par commandes:lancer_paiement.
    return redirect("paiements:success")


def paiement_success(request):
    return render(request, "paiements/success.html")


def paiement_failed(request):
    return render(request, "paiements/failed.html")
