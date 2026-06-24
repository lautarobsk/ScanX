from django.db import models

class Vehiculo(models.Model):
    patente = models.CharField(max_length=15, unique=True, db_index=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    sospechoso = models.BooleanField(default=False, db_index=True)
    fecha_alerta = models.DateTimeField(blank=True, null=True)


class Camara(models.Model):
    codigo_identificador = models.CharField(max_length=50, unique=True)
    direccion_aproximada = models.CharField(max_length=255, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    es_activa = models.BooleanField(default=True)




