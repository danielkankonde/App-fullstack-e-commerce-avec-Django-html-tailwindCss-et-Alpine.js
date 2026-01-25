from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid

from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Compte non activé. Vérifiez votre email.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'users/login.html')


# Dictionnaire pour stocker les tokens temporairement
activation_tokens = {}

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nom d'utilisateur déjà utilisé")
            return redirect('register')

        # Créer l'utilisateur mais inactif
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)

        # Créer un token unique
        token = str(uuid.uuid4())
        activation_tokens[token] = user.username

        # Lien d'activation
        activation_link = f"http://127.0.0.1:8000/users/activate/{token}/"

        # Envoyer email
        send_mail(
            'Activation de votre compte',
            f'Cliquez sur ce lien pour activer votre compte : {activation_link}',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings,'DEFAULT_FROM_EMAIL') else 'admin@example.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, "Compte créé ! Vérifiez votre email pour activer votre compte.")
        return redirect('login')

    return render(request, 'users/register.html')

def activate_user(request, token):
    username = activation_tokens.get(token)
    if username:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        messages.success(request, "Compte activé ! Vous pouvez maintenant vous connecter.")
        del activation_tokens[token]
    else:
        messages.error(request, "Lien d'activation invalide ou expiré.")
    return redirect('login')


def logout_view(request):
    return redirect('home')

