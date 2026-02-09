from django.db import models
from django.contrib.auth.models import User
from products.models import Produit

class Adresse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rue = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.rue}, {self.ville}"

class Commande(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('PAYEE', 'Payée'),
        ('EXPEDIEE', 'Expédiée'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    adresse = models.ForeignKey(Adresse, on_delete=models.SET_NULL, null=True)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id} - {self.user}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
