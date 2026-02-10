from django.urls import path
from . import views

app_name = "paiements"

urlpatterns = [
    path("callback/", views.paiement_callback, name="callback"),
    path('payer/<int:commande_id>/<str:methode>/', views.payer, name='payer'),
    path("success/", views.paiement_success, name="success"),
    path("failed/", views.paiement_failed, name="failed"),
]
