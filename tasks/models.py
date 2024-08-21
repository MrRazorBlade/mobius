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
    group_order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['group_order', 'group', 'due_date']
