from django.db import models
from commandes.models import Commande

class Paiement(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    mode_paiement = models.CharField(max_length=50)
    statut = models.CharField(max_length=50, default='En attente')
    reference_transaction = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.mode_paiement} - {self.statut}"
