from django.contrib import admin
from .models import Vehiculo, Camara, TramoCalle, RegistroDeteccion

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('patente', 'marca', 'modelo', 'sospechoso')
    search_fields = ('patente',)
    list_filter = ('sospechoso',)

@admin.register(Camara)
class CamaraAdmin(admin.ModelAdmin):
    # Actualizado con 'direccion' y 'activa'
    list_display = ('codigo_identificador', 'direccion', 'activa')
    search_fields = ('codigo_identificador',)
    list_filter = ('activa',)

@admin.register(TramoCalle)
class TramoCalleAdmin(admin.ModelAdmin):
    # Actualizado con 'distancia'
    list_display = ('origen', 'destino', 'nombre_calle', 'distancia')

@admin.register(RegistroDeteccion)
class RegistroDeteccionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'camara', 'timestamp', 'fecha_registro_sistema')
    list_filter = ('camara', 'timestamp')
    date_hierarchy = 'timestamp'