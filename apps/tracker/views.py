from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .models import Vehiculo, Camara, RegistroDeteccion
from .serializers import VehiculoSerializer, RegistroDeteccionSerializer


class IngestaDeteccionView(APIView):

    def post(self, request):
        # Extraemos los datos crudos que nos manda la cámara
        patente = request.data.get('patente_leida')
        codigo_camara = request.data.get('codigo_camara')
        timestamp_str = request.data.get('timestamp')

        if not all([patente, codigo_camara, timestamp_str]):
            return Response(
                {"error": "Faltan datos (patente_leida, codigo_camara, timestamp)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            camara = Camara.objects.get(codigo_identificador=codigo_camara)
            
            if not camara.activa:
                return Response({"error": "La cámara está inactiva"}, status=status.HTTP_403_FORBIDDEN)

            # Buscamos el vehículo, si es la primera vez que se lo ve, lo creamos al vuelo
            vehiculo, creado = Vehiculo.objects.get_or_create(
                patente=patente,
                defaults={'sospechoso': False}
            )

            timestamp = parse_datetime(timestamp_str)
            registro = RegistroDeteccion.objects.create(
                vehiculo=vehiculo,
                camara=camara,
                timestamp=timestamp
            )

            return Response({"mensaje": "Detección registrada con éxito"}, status=status.HTTP_201_CREATED)

        except Camara.DoesNotExist:
            return Response({"error": "Cámara no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistorialVehiculoView(APIView):

    def get(self, request, patente):
        try:
            detecciones = RegistroDeteccion.objects.filter(vehiculo__patente=patente)
            
            if not detecciones.exists():
                return Response(
                    {"mensaje": f"No se encontraron registros de detección de la patente : {patente}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = RegistroDeteccionSerializer(detecciones, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


