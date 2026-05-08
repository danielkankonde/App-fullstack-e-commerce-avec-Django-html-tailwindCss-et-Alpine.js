import uuid

import requests
from django.conf import settings

from .models import Paiement


class PaymentInitializationError(Exception):
    def __init__(self, user_message):
        super().__init__(user_message)
        self.user_message = user_message


def init_paiement(request, commande, methode):
    reference = str(uuid.uuid4())

    secret_key = getattr(settings, "FLUTTERWAVE_SECRET_KEY", None)
    if not secret_key or secret_key == "CLE_MANQUANTE":
        print("ERREUR : La cle FLUTTERWAVE_SECRET_KEY est absente du settings.py")
        raise PaymentInitializationError(
            "La cle secrete Flutterwave est absente dans settings.py."
        )

    Paiement.objects.create(
        user=request.user,
        commande=commande,
        methode=methode,
        reference=reference,
        montant=commande.prix_total,
        statut="EN_ATTENTE",
    )

    payload = {
        "tx_ref": reference,
        "amount": str(commande.prix_total),
        "currency": getattr(settings, "FLUTTERWAVE_CURRENCY", "USD"),
        "redirect_url": request.build_absolute_uri("/paiements/callback/"),
        "payment_options": methode,
        "customer": {
            "email": request.user.email or "client@email.com",
            "name": request.user.username,
        },
        "customizations": {
            "title": "Gstyle Shop",
            "description": f"Paiement Commande #{commande.id}",
        },
    }

    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://api.flutterwave.com/v3/payments",
            json=payload,
            headers=headers,
            timeout=10,
        )
        try:
            data = response.json()
        except ValueError as e:
            print(f"Reponse Flutterwave invalide : {response.text}")
            raise PaymentInitializationError(
                "Flutterwave a retourne une reponse illisible."
            ) from e

        if response.status_code == 200 and data.get("status") == "success":
            payment_link = data.get("data", {}).get("link")
            if payment_link:
                return payment_link

        print(f"Echec Flutterwave : {data}")
        message = data.get("message") or "Flutterwave a refuse la demande de paiement."
        raise PaymentInitializationError(message)
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion : {e}")
        raise PaymentInitializationError(
            "Impossible de joindre Flutterwave. Verifiez votre connexion Internet, votre DNS ou votre proxy."
        )
    except requests.exceptions.Timeout as e:
        print(f"Erreur de connexion : {e}")
        raise PaymentInitializationError(
            "Flutterwave ne repond pas pour le moment. Reessayez dans quelques instants."
        )
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
        raise PaymentInitializationError(
            "Une erreur reseau empeche la creation du paiement."
        )
