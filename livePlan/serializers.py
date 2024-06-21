# serializers.py
from rest_framework import serializers
from .models import planNegocio, inversionInicial, detalleInversionInicial

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
