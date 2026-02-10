import requests
from django.conf import settings
from django.shortcuts import redirect, render,get_object_or_404, redirect
from .models import Paiement
from django.utils import timezone
from commandes.models import Commande
import uuid

def paiement_callback(request):

    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")

    paiement = Paiement.objects.get(reference=tx_ref)

    # Vérifier le paiement côté Flutterwave
    response = requests.get(
        f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
        headers={
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"
        }
    )

    data = response.json()["data"]

    if data["status"] == "successful":
        paiement.statut = "PAYE"
        paiement.save()

        commande = paiement.commande
        commande.statut = "PAYÉ"
        commande.save()

        # Vider le panier
        panier = paiement.user.panier
        panier.lignepanier_set.all().delete()

        return redirect("paiements:success")

    paiement.statut = "ECHEC"
    paiement.save()
    return redirect("paiements:failed")



def payer(request, commande_id, methode):
    commande = get_object_or_404(Commande, id=commande_id)

    paiement = Paiement.objects.create(
        user=request.user,
        commande=commande,
        methode=methode,
        montant=commande.total,
        reference=str(uuid.uuid4()),
        statut='INITIE',
        date_creation=timezone.now()
    )

    # POUR TEST : on redirige vers une page succès
    return redirect('paiement_success')





def paiement_success(request):
    return render(request, "paiements/success.html")

def paiement_failed(request):
    return render(request, "paiements/failed.html")
