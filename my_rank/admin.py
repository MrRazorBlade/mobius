from django.contrib import admin
from .models import Rank


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    # Campos que deseas mostrar en la lista
    list_display = ('name', 'min_points', 'max_points', 'description')
