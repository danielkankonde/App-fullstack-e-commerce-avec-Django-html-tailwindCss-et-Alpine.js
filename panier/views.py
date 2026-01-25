from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Création des views
@login_required(login_url='login')
def cart_view(request):
    return render(request, 'panier/cart.html')
