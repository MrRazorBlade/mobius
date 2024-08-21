from django.db import models


class Task(models.Model):
    # Otros campos...
    group_order = models.IntegerField(default=0)
    # Ordenar por grupo y luego por el orden del grupo

    class Meta:
        ordering = ['group_order', 'group', 'due_date']
