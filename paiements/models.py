from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Paiement(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    methode = models.CharField(max_length=50)  # visa, mpesa, orange
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reference = models.CharField(max_length=100, blank=True)
    statut = models.CharField(max_length=50, default="EN_ATTENTE")
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Paiement {self.id} - {self.montant}"
