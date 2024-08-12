from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class THE_University(models.Model):
    rank = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    scores_overall = models.CharField(max_length=10)
    nid = models.IntegerField()
    location = models.CharField(max_length=255)
    subjects_offered = models.TextField()

    def __str__(self):
        return f"THE ranking; {self.name}; rank: {self.rank}"

class QS_University(models.Model):
    title = models.CharField(max_length=256)
    overall_score = models.FloatField(blank=True, null=True)
    rank = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    score_nid = models.CharField(max_length=255, unique=True, blank=True, null=True)  # Add the score_nid field

    def __str__(self):
        return f"QS ranking; {self.title}; rank: {self.rank}"
