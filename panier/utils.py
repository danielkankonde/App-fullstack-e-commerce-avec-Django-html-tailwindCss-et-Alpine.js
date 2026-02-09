from .models import Panier

# fonction pour récupérer ou créer un panier pour un utilisateur 
def get_or_create_panier(user):
    panier, created = Panier.objects.get_or_create(user=user)
    return panier
