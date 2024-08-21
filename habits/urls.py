from django.urls import path
from . import views

urlpatterns = [
    # Asegúrate de que esta línea existe
    path('', views.habit_list, name='habit_list'),
]
