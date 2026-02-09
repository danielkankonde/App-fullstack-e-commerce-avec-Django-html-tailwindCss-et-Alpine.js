from django.urls import path
from .views import paiement_callback

app_name = "paiements"

urlpatterns = [
    path("callback/", paiement_callback, name="callback"),
]
