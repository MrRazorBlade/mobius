from django.urls import path
from tasks.views import view_calendar  # Importa la vista desde tasks

urlpatterns = [
    path('', view_calendar, name='calendar'),
]
