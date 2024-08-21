from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('tasks/', include('tasks.urls')),
    path('calendar/', include('task_calendar.urls')),
    path('habits/', include('habits.urls')),
    path('flow/', include('flow.urls')),
    path('my_rank/', include('my_rank.urls')),
]
