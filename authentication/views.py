import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def github_login(request):
    github_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_KEY}"
        f"&scope=user:email"
    )
    return redirect(github_url)

def github_callback(request):
    code = request.GET.get("code")

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_KEY,
            "client_secret": settings.GITHUB_SECRET,
            "code": code,
        },
    )
    access_token = token_response.json().get("access_token")

    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    github_user = user_response.json()
    
    username = github_user["login"]
    email = github_user.get("email") or f"{username}@github.local"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email}
    )
    
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.profile.role,
    })