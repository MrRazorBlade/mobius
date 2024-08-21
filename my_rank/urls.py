from django.urls import path
from . import views

urlpatterns = [
    path('', views.rank_view, name='my_rank'),
]
