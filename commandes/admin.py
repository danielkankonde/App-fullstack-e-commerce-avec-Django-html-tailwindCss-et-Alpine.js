from django.contrib import admin
from .models import Adresse, Commande, LigneCommande

admin.site.register(Adresse)
admin.site.register(Commande)
admin.site.register(LigneCommande)
