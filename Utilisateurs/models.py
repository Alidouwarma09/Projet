# Utilisateurs/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q
from django.forms import forms
from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince
from multiupload.fields import MultiFileField


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

    def get_user_messages(self, user, recipient):
        return Message.objects.filter(Q(sender=user, receiver=recipient) | Q(sender=recipient, receiver=user))


class CustomUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    username = models.CharField(max_length=15, unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_logout = models.DateTimeField(default=timezone.now)
    unread_messages_count = models.IntegerField(default=0)

    @property
    def get_unread_messages(self):
        return Message.objects.filter(receiver=self, is_read=False).count()

    def time_since_last_logout(self):
        if self.last_logout:
            time_since_logout = timesince(self.last_logout)
            return f"En ligne il y a {time_since_logout}"
        else:
            return "Hors ligne (date de déconnexion non disponible)"

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f'{self.sender} to {self.receiver} ({self.timestamp})'


class BlogPost(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), related_name='blog_likes', blank=True)
    shares = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog_images/', verbose_name="Image d'accueil", blank=True)
    views = models.IntegerField(default=0)

    def get_delete_url(self):
        return reverse('delete_post', args=[str(self.id)])

    def increment_views(self):
        self.views += 1
        self.save()

    def get_like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Image {self.pk}"

    def time_pub_date_since(self):
        if self.pub_date:
            time_since_pub_date = timesince(self.pub_date)
            return f"Publier il y a {time_since_pub_date}"
        else:
            return "Hors ligne (date de déconnexion non disponible)"

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
