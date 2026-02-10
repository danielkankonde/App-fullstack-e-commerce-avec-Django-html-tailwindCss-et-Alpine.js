from django.db import models
from django.contrib.auth.models import User
from commandes.models import Commande

class Paiement(models.Model):
    METHODE_CHOICES = (
        ('card', 'Carte'),
        ('mobilemoney', 'Mobile Money'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name="paiements"
    )

    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    reference = models.CharField(max_length=100, unique=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=30, default="EN_ATTENTE")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.statut}"
