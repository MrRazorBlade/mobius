from django.urls import path
from . import views


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('calendar/', views.view_calendar, name='view_calendar'),
    path('toggle-task-completion/<int:task_id>/',
         views.toggle_task_completion, name='toggle_task_completion'),
    path('delete_completed/', views.delete_completed_tasks,
         name='delete_completed_tasks'),
    path('reorder/', views.reorder_groups, name='reorder_groups'),
]
