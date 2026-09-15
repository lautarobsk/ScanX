from apps.tracker.models import Vehiculo, Camara, TramoCalle, RegistroDeteccion
from rest_framework import serializers

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class CamaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camara
        fields = '__all__'

class TramoCalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TramoCalle
        fields = '__all__'
        

class RegistroDeteccionSerializer(serializers.ModelSerializer):

    camara_codigo = serializers.CharField(source='camara.codigo_identificador', read_only=True)
    latitud = serializers.CharField(source='camara.latitud', read_only=True)
    longitud = serializers.CharField(source='camara.longitud', read_only=True)
    direccion = serializers.CharField(source='camara.direccion', read_only=True)

    class Meta:
        model = RegistroDeteccion
        fields = ['id', 'timestamp', 'camara_codigo', 'latitud', 'longitud', 'direccion']
        read_only_fields = ['fecha_registro_sistema']



