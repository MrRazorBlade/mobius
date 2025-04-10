from django.conf import settings
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    group = models.CharField(max_length=100, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    # Evitar que el usuario burle el sistema
    reward_claimed = models.BooleanField(default=False)
    group_order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def complete_task(self):
        print(f"Intentando completar tarea: {self.title}, Completada: {self.completed}, Recompensa reclamada: {self.reward_claimed}")
        if not self.completed and not self.reward_claimed:
            self.completed = True
            self.reward_claimed = True  # Marca la recompensa como reclamada
            self.save()
            self.user.add_points(1)
            print(f"Puntos después de completar tarea: {self.user.points}")
            self.user.save()  # Asegurarse de guardar los cambios en el usuario
        else:
            print("La tarea ya fue completada o la recompensa ya fue reclamada.")

    class Meta:
        ordering = ['group_order', 'group', 'due_date']
