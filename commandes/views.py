from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout_view(request):
    return render(request, 'commandes/checkout.html')
