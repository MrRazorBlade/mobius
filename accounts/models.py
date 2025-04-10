# permite definir los modelos (las clases que se convertirán en tablas de base de datos).
from django.db import models
# Modelo para la creación de usuarios
from django.contrib.auth.models import AbstractUser
from my_rank.models import Rank


class CustomUser(AbstractUser):
    # Atributo para almacenar los puntos del usuario
    points = models.IntegerField(default=0)
    # Atributo para almacenar el rango del usuario
    rank = models.ForeignKey(
        Rank, on_delete=models.SET_NULL, null=True, blank=True)
    # Atributo para almacenar el tiempo de flow del usuario
    flow = models.FloatField(default=0.0)

    def __str__(self):
        return self.username  # Devuelve el nombre del usuario para mostrar en la lista de usuarios

    def save(self, *args, **kwargs):  # Se ejecuta antes de guardar el rango
        self.update_rank()  # Actualizar el rango antes de guardar
        super().save(*args, **kwargs)  # Llama al método save() de AbstractUser

    def add_points(self, points):  # Método para añadir puntos al usuario
        self.points += points
        self.update_rank()  # Actualizar el rango después de añadir puntos
        self.save()

    def update_rank(self):  # Método para actualizar el rango del usuario basado en sus puntos
        new_rank = Rank.objects.filter(
            min_points__lte=self.points).order_by('-min_points').first()
        # Busca el rango correcto basado en los puntos del usuario
        # Ordena los rangos por puntos en orden descendiente y devuelve

        # Si se encuentra un nuevo rango, y es diferente al actual, se actualiza el rango
        if new_rank and self.rank != new_rank:
            self.rank = new_rank
