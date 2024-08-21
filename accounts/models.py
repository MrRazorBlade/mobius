from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)
    rank = models.CharField(max_length=50, default='Novice')
    flow = models.FloatField(default=0.0)  # This replaces hours_worked

    def __str__(self):
        return self.username

    def add_points(self, points):
        self.points += points
        self.update_rank()
        self.save()

    def update_rank(self):
        if self.points >= 1000:
            self.rank = 'Expert'
        elif self.points >= 500:
            self.rank = 'Intermediate'
        else:
            self.rank = 'Novice'
