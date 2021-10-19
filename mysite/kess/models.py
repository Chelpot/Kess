import datetime
import uuid

from django.core.exceptions import ValidationError
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
    CELEBRITY = "Célébrités et personnages"
    ART = "Art et mode"


class Tile(models.Model):
    avatar = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    kessId = models.CharField(max_length=200, default='', blank=True)
    time = models.CharField(max_length=200)


class Kess(models.Model):
    emoji = models.CharField(max_length=200, unique=True, verbose_name='Kess?')
    reponse = models.CharField(max_length=200, verbose_name='Réponse')
    is_staff = models.BooleanField(default=False)
    is_ready_to_publish = models.BooleanField(default=False)
    published_at = models.DateTimeField('date published')
    created_at = models.DateTimeField('date created')
    created_by = models.CharField(max_length=200, default='anonyme')
    category = models.CharField(
        max_length=200,
        choices=[(tag.value, tag.value) for tag in CategoryChoice],
        default=CategoryChoice.DIVERS,
        verbose_name='Catégorie'
    )
    foundList = models.TextField(default='', blank=True)
    nbTries = models.IntegerField(default=None, blank=True, null=True)
    upVotes = models.TextField(default='', blank=True)
    downVotes = models.TextField(default='', blank=True)

    def __str__(self):
        return self.emoji

"""
================================================================================
USER PART
================================================================================
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


def is_ascii(s):
    if not all(ord(c) < 255 for c in s):
        raise ValidationError("Charactère(s) interdit(s) dans le pseudo, veuillez en choisir un autre")


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    avatar = models.CharField(max_length=1, default='🙂')
    name = models.CharField(max_length=32, blank=False, null=False, validators=[is_ascii], unique=True)
    points = models.IntegerField(default=None, blank=True, null=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    favs = models.TextField(default=None, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
