from django.urls import path
from .views import IngestaDeteccionView, HistorialVehiculoView, GetCamarasView

urlpatterns = [
    path('ingesta/', IngestaDeteccionView.as_view(), name='ingesta-deteccion'),
    path('historial/<str:patente>/', HistorialVehiculoView.as_view(), name='historial-vehiculo'),
    path('getCamaras/', GetCamarasView.as_view(), name='get-camaras')
]
