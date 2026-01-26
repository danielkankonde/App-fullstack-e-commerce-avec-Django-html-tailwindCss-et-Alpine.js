from django.shortcuts import render
from products.models import Categorie, Produit

def home(request):
    categories_populaires = Categorie.objects.filter(est_populaire=True)
    produits_populaires = Produit.objects.filter(est_populaire=True)[:8]

    context = {
        "categories": categories_populaires,
        "produits": produits_populaires,
    }
    return render(request, "home.html", context)
