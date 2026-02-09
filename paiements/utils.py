import uuid, requests
from django.conf import settings
from .models import Paiement

def init_paiement(request, commande, methode):
    reference = str(uuid.uuid4())

    Paiement.objects.create(
        user=request.user,
        commande=commande,
        methode=methode,
        reference=reference,
        montant=commande.prix_total,
        statut="PENDING"
    )

    payload = {
        "tx_ref": reference,
        "amount": str(commande.prix_total),
        "currency": "USD",
        "redirect_url": "http://127.0.0.1:8000/paiements/callback/",
        "payment_options": "card,mobilemoney",
        "customer": {
            "email": request.user.email,
            "name": request.user.username,
        },
        "customizations": {
            "title": "Gstyle Paiement",
            "description": "Paiement de votre commande"
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.flutterwave.com/v3/payments",
        json=payload,
        headers=headers
    )

    return response.json()["data"]["link"]
