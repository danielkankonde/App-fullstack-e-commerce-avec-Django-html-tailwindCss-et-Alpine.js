from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Produit

# Create your views here.
def product_list(request):
    produits = Produit.objects.all()

    context = {
        "produits": produits
    }
    return render(request, 'products/list_products.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    return render(request, 'products/detail_product.html', {
        'product': product
    })


