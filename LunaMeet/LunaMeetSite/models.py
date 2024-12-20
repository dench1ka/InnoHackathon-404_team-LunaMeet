from django.db import models
from django.db.models import Min, Max
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class Comments(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)


class Planed(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class Organizers(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Visited(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=400, default="")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons/', blank=True)

    organized_events_id = models.ManyToManyField('Event', through='Organizers', related_name='organized_event')
    visited_events_id = models.ManyToManyField('Event', through='Visited', related_name='visited_users')
    planed_events_id = models.ManyToManyField('Event', through='Planed', related_name='planed_users')
    commented_events_id = models.ManyToManyField('Event', through='Comments', related_name='commented_users')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    place = models.CharField(max_length=100, default='')

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True)
    organizers_id = models.ManyToManyField(User, through='Organizers', related_name='organized_events')
    visited_users_id = models.ManyToManyField(User, through='Visited', related_name='visited_events')
    planed_users_id = models.ManyToManyField(User, through='Planed', related_name='planed_events')
    commented_users_id = models.ManyToManyField(User, through='Comments', related_name='commented_events')
    created_at = models.DateTimeField(auto_now=True)
    reg_link = models.URLField(blank=True)

    def first_timecode(self):
        return self.time_codes.aggregate(Min('time'))['time__min']

    def last_timecode(self):
        return self.time_codes.aggregate(Max('time'))['time__max']

class TimeCod(models.Model):
    time = models.DateTimeField()
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="time_codes")

    def __str__(self):
        return f"{self.time} : {self.name}"


class Photos(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photos/')
