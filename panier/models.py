from django.db import models
from django.contrib.auth.models import User
from products.models import Produit

class Panier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier {self.id} - {self.user}"
    
    def total_items(self):
        return self.lignepanier_set.count()

class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
