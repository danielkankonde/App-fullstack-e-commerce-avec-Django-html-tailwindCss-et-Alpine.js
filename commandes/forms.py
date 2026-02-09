from django import forms
from .models import Adresse

class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = [
            "rue",
            "ville",
            "code_postal",
            "pays",
            "telephone"
        ]
        widgets = {
            "rue": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Rue / Avenue"
            }),
            "ville": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Ville"
            }),
            "code_postal": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Code postal"
            }),
            "pays": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Pays"
            }),
            "telephone": forms.TextInput(attrs={
                "class": "w-full p-2 border rounded",
                "placeholder": "Téléphone"
            }),
        }
