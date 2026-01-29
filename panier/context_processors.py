from .models import Panier

def panier_context(request):
    if request.user.is_authenticated:
        panier, _ = Panier.objects.get_or_create(user=request.user)
        return {'panier': panier}
    return {'panier': None}
