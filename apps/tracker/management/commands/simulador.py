import time
import random
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.tracker.models import Vehiculo, Camara, TramoCalle


### T0DO ESTE CODIGO FUE GENERADO POR IA PORQUE NO SABIA COMO HACER UN SIMULADOR

class Command(BaseCommand):
    help = 'Simula el movimiento de un vehículo por la red de cámaras.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando simulador de tráfico...'))

        if not Camara.objects.filter(activa=True).exists():
            self.stdout.write(self.style.ERROR('Error: No hay cámaras activas en la Base de Datos.'))
            return

        # Elegimos un vehículo al azar o se crea uno
        vehiculo = Vehiculo.objects.first()
        if not vehiculo:
            vehiculo = Vehiculo.objects.create(patente="SIM001", sospechoso=True)
            self.stdout.write(f'Vehículo de prueba creado: {vehiculo.patente}')

        # Elegimos una cámara de origen que tenga calles de salida
        tramos_disponibles = TramoCalle.objects.all()
        if not tramos_disponibles.exists():
            self.stdout.write(self.style.ERROR('Error: No hay calles (TramoCalle) conectando cámaras.'))
            return

        tramo_actual = random.choice(list(tramos_disponibles))
        camara_origen = tramo_actual.origen
        
        self.stdout.write(f'[{vehiculo.patente}] Aparece en la red: {camara_origen.codigo_identificador}')
        self._enviar_post(vehiculo.patente, camara_origen.codigo_identificador)

        # Iniciamos el ciclo infinito
        while True:
            # Buscamos todas las calles de salida desde la cámara donde estamos parados
            tramos_salida = TramoCalle.objects.filter(origen=camara_origen)
            
            if not tramos_salida.exists():
                self.stdout.write(self.style.WARNING(f'Callejón sin salida en {camara_origen.codigo_identificador}. Fin del trayecto.'))
                break # Rompe el ciclo si no hay a dónde ir

            # Elegimos un camino al azar para seguir escapando
            tramo_actual = random.choice(list(tramos_salida))
            camara_destino = tramo_actual.destino

            # Calculamos la física del tramo
            velocidad_simulada_kmh = random.uniform(30, 50)
            velocidad_ms = velocidad_simulada_kmh / 3.6
            tiempo_viaje_segundos = tramo_actual.distancia / velocidad_ms

            accion_texto = "Fugando" if vehiculo.sospechoso else "Circulando"
            
            self.stdout.write(self.style.WARNING(
                f'{accion_texto} por {tramo_actual.nombre_calle} hacia {camara_destino.codigo_identificador} '
                f'a {velocidad_simulada_kmh:.2f} km/h. ETA: {tiempo_viaje_segundos:.1f} seg...'
            ))

            # Congelamos el tiempo simulando el viaje
            time.sleep(tiempo_viaje_segundos)

            # Llegamos al nuevo nodo y disparamos a la API
            self.stdout.write(self.style.SUCCESS(f'[{vehiculo.patente}] Detectado en: {camara_destino.codigo_identificador}'))
            self._enviar_post(vehiculo.patente, camara_destino.codigo_identificador)

            # PREPARAR EL PRÓXIMO SALTO: El destino de hoy es el origen de mañana
            camara_origen = camara_destino

    def _enviar_post(self, patente, codigo_camara):
        """Función auxiliar que simula el disparo de hardware hacia la API"""
        url = 'http://127.0.0.1:8000/api/tracker/ingesta/'
        payload = {
            "patente_leida": patente,
            "codigo_camara": codigo_camara,
            "timestamp": timezone.now().isoformat()
        }
        
        try:
            # Hacemos la petición a nuestra propia API
            respuesta = requests.post(url, json=payload)
            if respuesta.status_code == 201:
                self.stdout.write(f'  -> API OK: Datos ingresados correctamente.')
            else:
                self.stdout.write(self.style.ERROR(f'  -> Error API: {respuesta.text}'))
        except requests.exceptions.ConnectionError:
            self.stdout.write(self.style.ERROR('  -> Error crítico: El servidor de la API no está corriendo.'))