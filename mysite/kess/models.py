import datetime
import uuid

from django.db import models
from enum import Enum

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class CategoryChoice(Enum):
    DIVERS = "Divers"
    GAMES = "Jeux vidéo"
    MOVIE = "Films et séries"
    EXPRESSION = "Expressions"
    CULINARY = "Alimentation"
    SPORT = "Sport"
    CELEBRITY = "Célébrités et personnages "


class Kess(models.Model):
    emoji = models.CharField(max_length=200, unique=True)
    reponse = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_ready_to_publish = models.BooleanField(default=False)
    published_at = models.DateTimeField('date published')
    created_at = models.DateTimeField('date created')
    category = models.CharField(
        max_length=200,
        choices=[(tag.value, tag.value) for tag in CategoryChoice],
        default=CategoryChoice.DIVERS
    )

    def __str__(self):
        return self.emoji

    """
    ==============================================================
    USER PART
    ==============================================================
    """


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            points=0,
            creation_date=datetime.datetime.now(),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=32, blank=False, null=False)
    points = models.IntegerField(default=None, blank=True, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
