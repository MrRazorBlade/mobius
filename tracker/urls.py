from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/', views.index, name='index'),
    path('toggle/<int:habit_id>/<int:day>/<int:month>/<int:year>/',
         views.toggle_habit_record, name='toggle_habit_record'),
    path('add/', views.add_habit, name='add_habit'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
]
