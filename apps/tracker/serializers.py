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
    class Meta:
        model = RegistroDeteccion
        fields = ['vehiculo', 'camara', 'timestamp', 'fecha_registro_sistema']
        read_only_fields = ['fecha_registro_sistema']



