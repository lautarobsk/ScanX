from django.db import models

class Vehiculo(models.Model):
    patente = models.CharField(max_length=15, unique=True, db_index=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    sospechoso = models.BooleanField(default=False, db_index=True)
    fecha_alerta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.patente} ({'ALERTA' if self.sospechoso else 'Ok'})"

class Camara(models.Model):
    codigo_identificador = models.CharField(max_length=50, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Cámara {self.codigo_identificador} - {self.direccion}"

class TramoCalle(models.Model):
    origen = models.ForeignKey(Camara, on_delete=models.CASCADE, related_name='tramos_salida')
    destino = models.ForeignKey(Camara, on_delete=models.CASCADE, related_name='tramos_entrada')
    nombre_calle = models.CharField(max_length=100, blank=True)
    distancia = models.PositiveIntegerField(help_text="Distancia entre las dos cámaras")
    velocidad_maxima = models.PositiveIntegerField(default=40, help_text="En km/h")

    class Meta:
        unique_together = ('origen', 'destino')

class RegistroDeteccion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='detecciones')
    camara = models.ForeignKey(Camara, on_delete=models.CASCADE, related_name='detecciones')
    timestamp = models.DateTimeField(db_index=True)
    fecha_registro_sistema = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.vehiculo.patente} en {self.camara.codigo_identificador}"


