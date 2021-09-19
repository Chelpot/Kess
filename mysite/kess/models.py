from django.db import models


class Kess(models.Model):
    emoji = models.CharField(max_length=200)
    reponse = models.CharField(max_length=200)
    isStaff = models.BooleanField()
    date = models.DateTimeField('date published')


def __str__(self):
    return self.emoji
