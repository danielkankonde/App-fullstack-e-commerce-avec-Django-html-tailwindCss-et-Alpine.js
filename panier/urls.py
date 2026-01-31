from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:produit_id>/', views.add_to_cart, name='add_to_cart'),
     path('increase/<int:ligne_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:ligne_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:ligne_id>/', views.remove_item, name='remove'),
]
