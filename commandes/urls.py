from django.urls import path
from commandes import views


app_name = "commande"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("payer/<int:commande_id>/", views.lancer_paiement, name="lancer_paiement"),
]
