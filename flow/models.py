from django.conf import settings
from django.db import models
from django.utils import timezone


class FlowSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    # Asegúrate de tener un campo para almacenar la duración
    duration = models.FloatField(default=0.0)

    def complete_flow(self):
        if not self.completed:
            self.end_time = timezone.now()

            # Convertir start_time a "aware" si es "naive"
            if timezone.is_naive(self.start_time):
                self.start_time = timezone.make_aware(
                    self.start_time, timezone.get_current_timezone())

            # Asegurarse de que end_time también sea "aware"
            if timezone.is_naive(self.end_time):
                self.end_time = timezone.make_aware(
                    self.end_time, timezone.get_current_timezone())

            # Calcular la duración en minutos
            self.duration = (
                self.end_time - self.start_time).total_seconds() / 60.0
            self.completed = True

            points = self.duration // 30  # Calcula cuántos puntos corresponden a la duración

            if points > 0:
                # Asegúrate de convertir a entero si es necesario
                self.user.add_points(int(points))

            self.save()
            self.user.save()  # Guarda los cambios en el usuario
            print(f"Puntos después de la sesión de flow: {self.user.points}")
