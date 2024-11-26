from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError
from . import models
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def send_confirm_email_request(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(reverse('confirm_email', kwargs={'uidb64': uid, 'token': token}))

    subject = 'Подтверждение регистрации'

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
                border-bottom: 1px solid #e0e0e0;
            }}
            .header h1 {{
                color: #333333;
                font-size: 24px;
                margin: 0;
            }}
            .content {{
                margin: 20px 0;
                color: #555555;
                font-size: 16px;
                line-height: 1.5;
            }}
            .button {{
                display: inline-block;
                background-color: #007BFF;
                color: #ffffff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
                margin: 10px 0;
            }}
            .footer {{
                text-align: center;
                color: #999999;
                font-size: 12px;
                margin-top: 20px;
                border-top: 1px solid #e0e0e0;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Добро пожаловать!</h1>
            </div>
            <div class="content">
                <p>Здравствуйте, {user.username}!</p>
                <p>Спасибо за регистрацию на нашем сайте. Пожалуйста, подтвердите ваш аккаунт, нажав на кнопку ниже:</p>
                <p style="text-align: center;">
                    <a href="{link}" class="button">Подтвердить аккаунт</a>
                </p>
                <p>Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.</p>
            </div>
            <div class="footer">
                <p>© 2024 Ваш сайт. Все права защищены.</p>
            </div>
        </div>
    </body>
    </html>
    """

    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email='your-email@gmail.com',
        to=[user.email],
    )
    email.content_subtype = 'html'
    email.send()


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(models.User, pk=uid)
    except (TypeError, ValueError, OverflowError):
        return JsonResponse({'error': 'Неверная ссылка'}, status=400)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return JsonResponse({'error': 'Ссылка недействительна'}, status=400)


def show_sign_up(request):
    return render(request, "registration.html")


def show_sign_in(request):
    return render(request, "login.html")


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

        if not user.is_active:
            return JsonResponse({"error": "Your account has not been verified, please check your email."}, status=403)

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
            user = models.User.objects.create_user(email=email, password=password, username=username, is_active=False)
            send_confirm_email_request(user, request)
            return JsonResponse({"message": "Please confirm your account, a message has been sent to your email."}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
