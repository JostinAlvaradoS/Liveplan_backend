from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from livePlan.auxiliares import calcular_ventas_mensuales
from .models import PrecioVenta, Producto_servicio, VariacionAnual, VentaDiaria, planNegocio, inversionInicial, detalleInversionInicial, proyeccionVentas
from .serializers import CostoSerializer, IndicadoresMacroSerializer, PlanNegocioSerializer, InversionInicialSerializer, DetalleInversionInicialSerializer, PrecioVentaSerializer, ProductoServicioSerializer, SupuestoSerializer, VariacionAnualSerializer, VentaDiariaSerializer

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

@api_view(['POST'])
def create_supuesto(request):
    if request.method == 'POST':
        serializer = SupuestoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_producto_servicio(request):
    if request.method == 'POST':
        serializer = ProductoServicioSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save() 
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_venta_diaria(request):
    if request.method == 'POST':
        serializer = VentaDiariaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_variacion_anual(request):
    if request.method == 'POST':
        serializer = VariacionAnualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_precios(request):
    if request.method == 'POST':
        serializer = PrecioVentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_costos(request):
    if request.method == 'POST':
        serializer = CostoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def obtener_proyeccion_demanda(request):
    try:
        plan_negocio_id = request.data.get('planNegocio')
        plan = planNegocio.objects.get(id=plan_negocio_id)
        productos = Producto_servicio.objects.filter(planNegocio=plan)
        variaciones_anuales = VariacionAnual.objects.filter(planNegocio=plan).order_by('anio')
        ventas_diarias = VentaDiaria.objects.filter(planNegocio=plan)

        respuesta = {}

        # Inicializar ventas para el primer año
        ventas_anio_anterior = {}
        for producto in productos:
            ventas_por_dia = ventas_diarias.get(producto_servicio=producto).ventas_por_dia
            ventas_anio_anterior[producto.id] = calcular_ventas_mensuales(ventas_por_dia, 0)

        for anio in sorted(set(v.anio for v in variaciones_anuales)):
            if anio not in respuesta:
                respuesta[anio] = []

            # Filtrar variaciones para el año actual
            variaciones_anio_actual = variaciones_anuales.filter(anio=anio)
            
            for producto in productos:
                # Obtener el porcentaje de crecimiento para el año actual
                variacion_producto = variaciones_anio_actual.first() # Usar la primera variación disponible
                porcentaje_variacion = variacion_producto.porcentaje if variacion_producto else 0

                # Calcular ventas mensuales para el año actual
                ventas_por_dia_anterior = ventas_anio_anterior[producto.id]
                ventas_mensuales_actual = [venta_mes_anterior * (1 + (porcentaje_variacion / 100)) for venta_mes_anterior in ventas_por_dia_anterior]

                producto_data = {
                    "idProd":producto.id,
                    "nombre": producto.nombre,
                    "porcentaje": porcentaje_variacion,
                    "ventas_mensuales": ventas_mensuales_actual
                }

                respuesta[anio].append(producto_data)

                proyeccionVentas.objects.update_or_create(
                    planNegocio=plan,
                    producto_servicio=producto,
                    anio=anio,
                    defaults={'ventas_mensuales': ventas_mensuales_actual}
                )

                ventas_anio_anterior[producto.id] = ventas_mensuales_actual

        return Response(respuesta)

    except planNegocio.DoesNotExist:
        return Response({"error": "Plan de negocio no encontrado."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
def create_indicadores_macro(request):
    if request.method == 'POST':
        serializer = IndicadoresMacroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


@api_view(['POST'])
def calcular_ventas(request):
    try:
        # Obtener el ID del plan de negocio del cuerpo de la solicitud POST
        plan_negocio_id = request.data.get('planNegocio')
        
        # Verificar si se proporcionó el ID
        if not plan_negocio_id:
            return Response({"error": "El ID del plan de negocio es requerido."}, status=400)
        
        plan = planNegocio.objects.get(id=plan_negocio_id)
        productos = Producto_servicio.objects.filter(planNegocio=plan)
        
        resultados = {"resultado": {}}
        num_anios = 5  # Número de años

        for producto in productos:
            try:
                # Buscar proyecciones de ventas para el producto
                proyecciones = proyeccionVentas.objects.filter(planNegocio=plan, producto_servicio=producto)
                
                if not proyecciones:
                    resultados["resultado"][producto.nombre] = {"error": "No se encontraron proyecciones de ventas para este producto."}
                    continue
                
                # Inicializar los valores de ventas mensuales por año
                ventas_mensuales_totales = {f"Año {anio+1}": {str(mes): 0 for mes in range(1, 13)} for anio in range(num_anios)}
                
                for proyeccion in proyecciones:
                    ventas_mensuales = proyeccion.ventas_mensuales  # Esto es un JSONField
                    
                    # Verificar que ventas_mensuales sea una lista de 12 elementos
                    if isinstance(ventas_mensuales, list) and len(ventas_mensuales) == 12:
                        ventas_mensuales_por_30 = [venta * 30 for venta in ventas_mensuales]
                        anio_index = proyeccion.anio - 1
                        if 0 <= anio_index < num_anios:
                            for mes, venta in enumerate(ventas_mensuales_por_30, start=1):
                                ventas_mensuales_totales[f"Año {anio_index+1}"][str(mes)] += venta
                                
                # Calcular el total anual para cada año
                totales_anuales = {anio: sum(ventas_mensuales_totales[anio][str(mes)] for mes in range(1, 13)) for anio in ventas_mensuales_totales}
                
                # Agregar los resultados para cada producto
                resultados["resultado"][producto.nombre] = {
                    "ventas_mensuales": ventas_mensuales_totales,
                    "totales_anuales": totales_anuales,
                }
            
            except Exception as e:
                # Manejar cualquier excepción durante el procesamiento
                resultados["resultado"][producto.nombre] = {"error": str(e)}

        return Response(resultados)

    except planNegocio.DoesNotExist:
        return Response({"error": "Plan de negocio no encontrado."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)