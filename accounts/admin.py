from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Mostrar estos campos en la lista de usuarios en la página de admin
    list_display = ["email", "username", "points", "rank"]

    # Búsqueda por estos campos a los usuarios desde la página de admin
    search_fields = ["email", "username"]

    # Filtro por rango en la lista de usuarios desde la página de admin
    list_filter = ["rank"]

    # Mostrar estos campos en el formulario de edición de usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("points", "rank")}),
    )

    # Mostrar estos campos en el formulario de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("points", "rank")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
