# serializers.py
from rest_framework import serializers
from .models import Costo, IndicadoresMacro, PrecioVenta, Producto_servicio, planNegocio, inversionInicial, detalleInversionInicial,Supuesto, VentaDiaria, VariacionAnual

class PlanNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = planNegocio
        fields = '__all__'

class InversionInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = inversionInicial
        fields = '__all__'

class DetalleInversionInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = detalleInversionInicial
        fields = '__all__'


class SupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supuesto
        fields = '__all__'

class ProductoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto_servicio
        fields = '__all__'

class VentaDiariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDiaria
        fields = '__all__'

class VariacionAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariacionAnual
        fields = '__all__'


class PrecioVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioVenta
        fields = '__all__'

class CostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costo
        fields = '__all__'


class IndicadoresMacroSerializer(serializers.ModelSerializer):
     class Meta:
        model = IndicadoresMacro
        fields = '__all__'