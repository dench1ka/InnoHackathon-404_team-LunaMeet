from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError
from . import models
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.models import Token


# Create your views here.
def show_sign_up(request):
    return render(request, "registration.html")


def show_sign_in(request):
    return render(request, "login.html")

def show_eventpage(request):
    return render(request, "eventpage.html")

def show_profile(request):
    return render(request, "profile.html")


def main_page(request):
    return render(request, 'main_page.html')


@csrf_protect
def login(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({"error": "All fields are required."}, status=400)

        user = models.User.objects.filter(email=email).first()

        if user is None:
            return JsonResponse({"error": "User with that email doesn't exist."}, status=404)

        if not (user.check_password(password)):
            return JsonResponse({"error": "Invalid email or password."}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'message': 'User login successfully', "token": token.key}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_protect
def register(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        username = request.POST.get("username")

        if not email or not password or not confirm_password or not username:
            return JsonResponse({"error": "All fields are required."}, status=400)

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match."}, status=400)

        if models.User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already in use."}, status=400)

        if models.User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username is already in use."}, status=400)

        try:
            user = models.User.objects.create_user(email=email, password=password, username=username)
            return JsonResponse({"message": "User registered successfully."}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
