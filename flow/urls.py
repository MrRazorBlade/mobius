from django.urls import path
from .views import assign_point, flow

urlpatterns = [
    path('', flow, name='flow'),
    path('assign-point/', assign_point, name='assign_point'),
]
