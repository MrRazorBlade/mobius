from django.db import models


class Rank(models.Model):
    name = models.CharField(max_length=100)
    min_points = models.IntegerField()
    max_points = models.IntegerField(
        null=True, blank=True)  # Permitir valores nulos
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
