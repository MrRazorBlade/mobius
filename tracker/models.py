from django.conf import settings
from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # Relaciona el hábito con el usuario
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    # Comprueba que la recompnesa ha sido reclamada
    reward_claimed = models.BooleanField(default=False)

    class Meta:
        # Asegura que no se pueda tener más de un registro para
        # un hábito en una fecha específica
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} on {self.date}"

    def complete_habit(self):
        if not self.completed and not self.reward_claimed:
            self.completed = True
            self.reward_claimed = True  # Marca la recompensa como reclamada
            self.save()
            self.habit.user.add_points(1)
            self.habit.user.save()  # Asegurarse de guardar los cambios en el usuario
        else:
            print("El hábito ya fue completado o la recompensa ya fue reclamada.")
