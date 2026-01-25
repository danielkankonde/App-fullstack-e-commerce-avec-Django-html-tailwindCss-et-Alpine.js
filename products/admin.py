from django.contrib import admin
from .models import Produit, Categorie

admin.site.register(Categorie)
admin.site.register(Produit)
