from django.urls import path
from .views import checkout

app_name = "commande"

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
]
