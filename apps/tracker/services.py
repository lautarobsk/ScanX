from datetime import timedelta
from apps.tracker.models import TramoCalle

class MotorPrediccionService:
    def __init__(self, factor_fuga=2.0):
        self.factor_fuga = factor_fuga   #factor que asume que el sospechoso va al doble de la velocidad maxima
      
    def calcular_nodos_probables(self, ultima_deteccion):

        camara_origen = ultima_deteccion.camara
        tiempo_inicial = ultima_deteccion.timestamp

        calles_disponibles = TramoCalle.objects.filter(origen=camara_origen)


        predicciones = []

        for calle in calles_disponibles:
            vel_legal_ms = (calle.velocidad_maxima * 1000) / 3600

            vel_fuga_ms = vel_legal_ms * self.factor_fuga

            segundos_min = calle.distancia / vel_fuga_ms
            segundos_max = calle.distancia / vel_legal_ms

            tiempo_min = tiempo_inicial + timedelta(seconds=segundos_min)
            tiempo_max = tiempo_inicial + timedelta(seconds=segundos_max)

            predicciones.append({
            'camara_destino': calle.destino.codigo_identificador,
            'calle': calle.nombre_calle,
            'ventana_llegada': {
                'desde': tiempo_min,
                'hasta': tiempo_max
            }
        })

        return predicciones
