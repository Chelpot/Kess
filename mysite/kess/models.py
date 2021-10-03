from django.db import models
from enum import Enum

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


