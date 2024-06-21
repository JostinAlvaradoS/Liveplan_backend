from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlanNegocioSerializer, InversionInicialSerializer, DetalleInversionInicialSerializer

@api_view(['POST'])
def create_plan_negocio(request):
    if request.method == 'POST':
        serializer = PlanNegocioSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save() 
            response_data = serializer.data
            response_data['id'] = instance.id  
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_inversion_inicial(request):
    if request.method == 'POST':
        serializer = InversionInicialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_detalle_inversion_inicial(request):
    if request.method == 'POST':
        serializer = DetalleInversionInicialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
