from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    est_populaire = models.BooleanField(default=False)

    def __str__(self):
        return self.nom



class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    est_populaire = models.BooleanField(default=False)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom
