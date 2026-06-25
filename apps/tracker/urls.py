from django.urls import path
from .views import IngestaDeteccionView

urlpatterns = [
    path('ingesta/', IngestaDeteccionView.as_view(), name='ingesta-deteccion'),
]