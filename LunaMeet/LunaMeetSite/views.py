import json
from . import models
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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


def show_eventpage(request, event_id):
    if request.method == "GET":
        event = models.Event.objects.get(id=event_id)
        return render(request, "eventpage.html", {"event": event})
    return JsonResponse({"error": "Invalid request method."}, status=405)


def show_profile(request):
    return render(request, "profile.html")


@csrf_protect
def add_comment(request: HttpRequest):
    if request.method == "POST":
        token = request.POST.get('token')
        event_id = request.POST.get('event_id')
        comment = request.POST.get('comment')

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({"error": "User doesn't authorize"}, status=403)

        user = token.user
        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return JsonResponse({"error": "User doesn't authorize"}, status=404)

        models.Comments.objects.create(event=event, user=user, text=comment)

        return JsonResponse({}, status=201)


def main_page(request):
    if request.method == 'GET':
        categories = models.Category.objects.all()

        categorized_events = []
        for category in categories:
            events = models.Event.objects.filter(category=category).order_by('-created_at')[:6]
            if events.exists():
                categorized_events.append({
                    "category_name": category.name,
                    "events": events
                })

        return render(request, 'main_page.html', {"categorized_events": categorized_events})

    return JsonResponse({"error": "Invalid request method."}, status=405)

def search(request: HttpRequest):
    if request.method == 'GET':
        query = request.GET.get('query')

        if query == "None":
            return render(request, 'search.html', {"events": models.Event.objects.all()})

        events = (
            models.Event.objects.filter(name__icontains=query) |
            models.Event.objects.filter(category__name__icontains=query) |
            models.Event.objects.filter(place__icontains=query)
        ).distinct()

        return render(request, 'search.html', {"events": events})

    return JsonResponse({"error": "Invalid request method."}, status=405)


def show_add_event(request):
    return render(request, "add_event.html", {"categories": models.Category.objects.all()})


def user(request, token):
    if request.method == 'GET':
        try:
            token = Token.objects.get(key=token)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({"error": "User doesn't authorize"}, status=403)

        planned_events = user.planed_events_id.all()
        visited_events = user.visited_events_id.all()

        context = {
            "user": user,
            "planned_events": planned_events,
            "visited_events": visited_events,
        }
        return render(request, 'profile.html', context)

    return JsonResponse({"error": "Invalid request method."}, status=405)


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


@csrf_protect
def add_event(request: HttpRequest):
    if request.method == 'POST':
        # Получаем обычные поля формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        place = request.POST.get('place')
        category = request.POST.get('category')
        category = models.Category.objects.get(name=category)

        # Получаем массивы данных (организаторы и временные метки)
        organizers = request.POST.getlist('organizers[]')  # Список организаторов
        timecods = request.POST.getlist('timecods[]')      # Список временных меток

        # Получаем файлы
        photos = request.FILES.getlist('photos')  # Список файлов

        # Создаем событие
        event = models.Event.objects.create(
            name=name,
            description=description,
            place=place,
            category=category,
        )

        event.save()

        # Добавляем организаторов
        for organizer_name in organizers:
            user = models.User.objects.filter(username=organizer_name).first()
            if user:
                models.Organizers.objects.create(event=event, user=user)

        # Добавляем временные метки
        for timecod in timecods:
            timecod_name, timecod_date = timecod.split(" - ", 1)  # Разбираем временную метку
            models.TimeCod.objects.create(event=event, name=timecod_name, time=timecod_date)

        # Сохраняем фотографии
        for photo in photos:
            models.Photos.objects.create(event=event, photo=photo)

        event.save()

        return JsonResponse({"message": "Event created successfully."}, status=201)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def mark_event(request: HttpRequest):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            mark = data.get("value")
            event_id = data.get("event_id")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        token = request.headers.get("Authorization")

        try:
            event = models.Event.objects.get(id=event_id)
        except models.Event.DoesNotExist:
            return JsonResponse({"error": "Event doesn't exist."}, status=404)

        try:
            token = Token.objects.get(key=token)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({"error": "Invalid token."}, status=403)

        if mark == "Не был(а)":
            models.Planed.objects.filter(user=user, event=event).delete()
            models.Visited.objects.filter(user=user, event=event).delete()
        elif mark == "Был(а)":
            models.Planed.objects.filter(user=user, event=event).delete()
            models.Visited.objects.create(user=user, event=event)
        elif mark == "Планирую":
            models.Visited.objects.filter(user=user, event=event).delete()
            models.Planed.objects.create(user=user, event=event)

        return JsonResponse({"message": "Mark was changed."}, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_user_by_username(request: HttpRequest):
    if request.method == 'GET':
        username = request.GET.get('username')

        user = models.User.objects.filter(username=username).first()

        if user and user.is_active:
            return JsonResponse({"message": "User exists."}, status=200)

        return JsonResponse({"error": "User doesn't exists."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_user_details_by_token(request: HttpRequest, event_id):
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        event = models.Event.objects.filter(id=event_id).first()

        if not event:
            return JsonResponse({"error": "Event doesn't exists."}, status=404)

        if not token:
            return JsonResponse({"error": "Authorization header is missing"}, status=403)

        try:
            token = Token.objects.get(key=token)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({"error": "Invalid token."}, status=403)

        if models.Planed.objects.filter(user=user, event=event).exists():
            mark = "Планирую"
        elif models.Visited.objects.filter(user=user, event=event).exists():
            mark = "Был(а)"
        else:
            mark = "Не был(а)"

        return JsonResponse({
            "username": user.username,
            "icon": user.icon.url if user.icon else None,
            "mark": mark
        }, status=200)

    return JsonResponse({"error": "Invalid request method."}, status=405)
