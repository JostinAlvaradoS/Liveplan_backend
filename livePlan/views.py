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
    print('Request Data:', request.data)
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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import planNegocio, inversionInicial, detalleInversionInicial
from .serializers import PlanNegocioSerializer, InversionInicialSerializer, DetalleInversionInicialSerializer

@api_view(['POST'])
def get_plan_negocio_by_autor(request):
    autor = request.data.get('autor')
    if autor is not None:
        plans = planNegocio.objects.filter(autor=autor)
        serializer = PlanNegocioSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "Autor not provided"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_inversion_inicial_by_plan_negocio(request):
    plan_negocio_id = request.data.get('planNegocio')
    if plan_negocio_id is not None:
        inversiones = inversionInicial.objects.filter(planNegocio_id=plan_negocio_id)
        response_data = []
        for inversion in inversiones:
            detalle = get_detalle_inversion_inicial(inversion.id)
            response_data.append({
                'seccion': inversion.seccion,
                'importe': inversion.importe,
                'detalle': detalle
            })
        return Response(response_data, status=status.HTTP_200_OK)
    return Response({"error": "PlanNegocio ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


def get_detalle_inversion_inicial(seccion_id):
    detalles = detalleInversionInicial.objects.filter(seccion_id=seccion_id)
    return DetalleInversionInicialSerializer(detalles, many=True).data