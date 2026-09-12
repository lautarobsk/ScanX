from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Vehiculo, Camara, RegistroDeteccion
from .serializers import RegistroDeteccionSerializer, CamaraSerializer
from .services import MotorPrediccionService
from django.utils.timezone import localtime
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import DjangoModelPermissions

class IngestaDeteccionView(APIView):

    def post(self, request):
        patente = request.data.get('patente_leida')
        codigo_camara = request.data.get('codigo_camara')
        timestamp_str = request.data.get('timestamp')

        if not all([patente, codigo_camara, timestamp_str]):
            return Response(
                {"error": "Faltan datos (patente_leida, codigo_camara, timestamp)"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            camara = Camara.objects.get(codigo_identificador=codigo_camara)
            
            if not camara.activa:
                return Response({"error": "La cámara está inactiva"}, status=status.HTTP_403_FORBIDDEN)
            
            vehiculo, creado = Vehiculo.objects.get_or_create(patente=patente, defaults={'sospechoso': False})

            timestamp = parse_datetime(timestamp_str)
            registro = RegistroDeteccion.objects.create(
                vehiculo=vehiculo,
                camara=camara,
                timestamp=timestamp
            )

            respuesta_data = {"mensaje": "Detección registrada con éxito"}

            if vehiculo.sospechoso:
                motor = MotorPrediccionService(factor_fuga=2.0)
                predicciones = motor.calcular_nodos_probables(registro)
                
                respuesta_data["ALERTA SOSPECHOSO"] = True
                respuesta_data["predicciones_escape"] = predicciones
                
                print(f"¡ALERTA! Auto sospechoso detectado: {vehiculo.patente}")
                print(f"Último avistamiento: {camara.codigo_identificador} ({camara.direccion})")
                print("Cámaras de bloqueo recomendadas:")
                for p in predicciones:
                    llegada_desde = localtime(p['ventana_llegada']['desde'])
                    llegada_hasta = localtime(p['ventana_llegada']['hasta'])

                    t_desde = llegada_desde.strftime('%H:%M:%S')
                    t_hasta = llegada_hasta.strftime('%H:%M:%S')

                    print(f" -> {p['camara_destino']} por calle {p['calle']}")
                    print(f"    Tiempo de intercepción {t_desde} y las {t_hasta}")
                    print("\n\n\n")



            return Response(respuesta_data, status=status.HTTP_201_CREATED)

        except Camara.DoesNotExist:
            return Response({"error": "Cámara no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistorialVehiculoView(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = RegistroDeteccion.objects.none()
    
    def get(self, request, patente):
        tiempo_limite = timezone.now() - timedelta(hours=2000)
        try:
            detecciones = RegistroDeteccion.objects.filter(vehiculo__patente=patente, timestamp__gte=tiempo_limite)
            
            if not detecciones.exists():
                return Response(
                    {"mensaje": f"No se encontraron registros de detección de la patente : {patente}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = RegistroDeteccionSerializer(detecciones, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCamarasView(APIView):
    def get(self, request, format=None):
        camaras = Camara.objects.all()
        serializer = CamaraSerializer(camaras, many=True)
        return Response(serializer.data)