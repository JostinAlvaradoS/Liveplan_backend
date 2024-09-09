from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from livePlan.auxiliares import calcular_ventas_mensuales
from .models import Categorias_costos, Costo, PrecioVenta, Producto_servicio, VariacionAnual, VentaDiaria, depreciacionMensual, planNegocio, inversionInicial, detalleInversionInicial, proyeccionVentas
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
    

@api_view(['POST'])
def update_vida_util(request):
    try:
        id = request.data.get('id')
        if not id:
            return Response({"error": "El ID es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener el detalle de inversión inicial
        detalle = detalleInversionInicial.objects.get(id=id)
        
        # Obtener el nuevo valor de vida útil
        vida_util = int(request.data.get('vida_util', None))

        if vida_util is not None:
            # Actualizar vida útil en detalle de inversión
            detalle.vida_util = vida_util
            detalle.save()
            
            # Obtener el importe del detalle de inversión
            importe = detalle.importe
            
            # Calcular la depreciación mensual y anual
            if vida_util > 0:
                depreciacion_mensual = importe / vida_util
                depreciacion_anual = depreciacion_mensual * 12
                depreciacion_anio1 = depreciacion_anual
                depreciacion_anio2 = depreciacion_anual
                depreciacion_anio3 = depreciacion_anual
                depreciacion_anio4 = depreciacion_anual
                depreciacion_anio5 = depreciacion_anual
                
                # Calcular el valor de rescate
                total_depreciacion = depreciacion_anio1 + depreciacion_anio2 + depreciacion_anio3 + depreciacion_anio4 + depreciacion_anio5
                valor_rescate = importe - total_depreciacion
                
                # Actualizar la depreciación mensual para el detalle de inversión
                depreciaciones = depreciacionMensual.objects.filter(inversion=detalle)
                
                for depreciacion in depreciaciones:
                    depreciacion.depreciacionMensual = depreciacion_mensual
                    depreciacion.depreciacion_anio1 = depreciacion_anio1
                    depreciacion.depreciacion_anio2 = depreciacion_anio2
                    depreciacion.depreciacion_anio3 = depreciacion_anio3
                    depreciacion.depreciacion_anio4 = depreciacion_anio4
                    depreciacion.depreciacion_anio5 = depreciacion_anio5
                    depreciacion.valor_rescate = valor_rescate
                    depreciacion.save()
            
            # Serializar el detalle de inversión actualizado
            serializer = DetalleInversionInicialSerializer(detalle)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"error": "El campo vida_util es requerido."}, status=status.HTTP_400_BAD_REQUEST)
    
    except detalleInversionInicial.DoesNotExist:
        return Response({"error": "El detalle de la inversión inicial no fue encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def gestionar_depreciacion_mensual(request):
 if request.method == 'POST':
        # Obtener el ID del plan de negocio del cuerpo de la solicitud POST
        plan_negocio_id = request.data.get('planNegocio')
        
        # Verificar si se proporcionó el ID
        if not plan_negocio_id:
            return Response({"error": "El ID del plan de negocio es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener el plan de negocio
            plan = planNegocio.objects.get(id=plan_negocio_id)
        except planNegocio.DoesNotExist:
            return Response({"error": "Plan de negocio no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener todas las secciones para el plan de negocio
        secciones = inversionInicial.objects.filter(planNegocio=plan)
        
        if not secciones.exists():
            return Response({"error": "No se encontraron secciones para este plan de negocio."}, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar depreciaciones existentes
        depreciaciones_existentes = depreciacionMensual.objects.filter(planNegocio=plan)
        
        if depreciaciones_existentes.exists():
            # Crear un diccionario para los resultados
            resultados = {}
            
            for seccion in secciones:
                detalles = detalleInversionInicial.objects.filter(seccion=seccion)
                detalles_datos = []
                
                for detalle in detalles:
                    depreciaciones = depreciacionMensual.objects.filter(inversion=detalle)
                    depreciaciones_datos = [
                        {
                            "id": dep.id,
                            "depreciacionMensual": dep.depreciacionMensual,
                            "depreciacion_anio1": dep.depreciacion_anio1,
                            "depreciacion_anio2": dep.depreciacion_anio2,
                            "depreciacion_anio3": dep.depreciacion_anio3,
                            "depreciacion_anio4": dep.depreciacion_anio4,
                            "depreciacion_anio5": dep.depreciacion_anio5,
                            "valor_rescate": dep.valor_rescate
                        }
                        for dep in depreciaciones
                    ]
                    detalles_datos.append({
                        "id": detalle.id,
                        "nombre":detalle.elemento,
                        "importe":detalle.importe,
                        "vida_util": detalle.vida_util,
                        "depreciaciones": depreciaciones_datos
                    })
                
                resultados[f"{seccion.seccion}"] = {
                    "importe_total": seccion.importe,
                    "detalles": detalles_datos
                }
            
            return Response(resultados, status=status.HTTP_200_OK)
        else:
            # Crear depreciaciones si no existen
            for seccion in inversionInicial.objects.filter(planNegocio=plan):
                detalles = detalleInversionInicial.objects.filter(seccion=seccion)
                
                for detalle in detalles:
                    if not depreciacionMensual.objects.filter(planNegocio=plan, inversion=detalle).exists():
                        depreciacionMensual.objects.create(
                            planNegocio=plan,
                            inversion=detalle,
                            depreciacionMensual=None,
                            depreciacion_anio1=None,
                            depreciacion_anio2=None,
                            depreciacion_anio3=None,
                            depreciacion_anio4=None,
                            depreciacion_anio5=None,
                            valor_rescate=None
                        )
            
            # Devolver los datos recién creados
            return Response({"mensaje": "Depreciaciones creadas exitosamente."}, status=status.HTTP_201_CREATED)
        

@api_view(['POST'])
def generar_tabla_precios(request):
    try:
        # Obtener el ID del plan de negocio desde la solicitud
        plan_negocio_id = request.data.get('planNegocio')
        if not plan_negocio_id:
            return Response({"error": "El planNegocio es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el plan de negocio existe
        try:
            plan_negocio = planNegocio.objects.get(id=plan_negocio_id)
        except planNegocio.DoesNotExist:
            return Response({"error": "El plan de negocio no fue encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los productos o servicios asociados al plan de negocio
        productos = Producto_servicio.objects.filter(planNegocio=plan_negocio)

        # Si no hay productos, retornar un error
        if not productos.exists():
            return Response({"error": "No se encontraron productos o servicios para este plan de negocio."}, status=status.HTTP_404_NOT_FOUND)

        # Estructura de la tabla de precios
        tabla_precios = {}

        for producto in productos:
            # Obtener el precio del producto
            try:
                precio = PrecioVenta.objects.get(planNegocio=plan_negocio, producto_servicio=producto).precio
            except PrecioVenta.DoesNotExist:
                continue  # Saltar si no hay precio para este producto

            # Inicializar datos para el producto actual
            datos_producto = {
                "ventas_mensuales": {},
                "totales_anuales": {}
            }

            # Repetir el precio mensual durante 5 años y calcular los totales anuales
            for anio in range(1, 6):
                total_anio = 0
                datos_producto["ventas_mensuales"][f"Año {anio}"] = {}
                for mes in range(1, 13):
                    # Asignar el precio mensual
                    datos_producto["ventas_mensuales"][f"Año {anio}"][str(mes)] = precio
                    total_anio += precio/12  # Acumular el total para el año

                # Al final de cada año, asignar el total anual
                datos_producto["totales_anuales"][f"Año {anio}"] = total_anio

            # Agregar el producto con su tabla de precios al resultado final
            tabla_precios[producto.nombre] = datos_producto

        # Retornar el JSON estructurado de la forma solicitada
        return Response({"resultado": tabla_precios}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generar_reporte_costos(request):
    try:
        # Obtener el ID del plan de negocio desde la solicitud
        plan_negocio_id = request.data.get('planNegocio')
        if not plan_negocio_id:
            return Response({"error": "El planNegocio es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el plan de negocio existe
        try:
            plan_negocio = planNegocio.objects.get(id=plan_negocio_id)
        except planNegocio.DoesNotExist:
            return Response({"error": "El plan de negocio no fue encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los productos o servicios asociados al plan de negocio
        productos = Producto_servicio.objects.filter(planNegocio=plan_negocio)

        # Si no hay productos, retornar un error
        if not productos.exists():
            return Response({"error": "No se encontraron productos o servicios para este plan de negocio."}, status=status.HTTP_404_NOT_FOUND)

        # Estructura del reporte de costos
        reporte_costos = {}

        for producto in productos:
            # Inicializar datos para el producto actual
            datos_producto = {}

            # Obtener todas las categorías de costos asociadas al producto
            costos_producto = Costo.objects.filter(planNegocio=plan_negocio, producto_servicio=producto)

            # Agrupar los costos por categoría
            for categoria in Categorias_costos.objects.all():
                costos_categoria = costos_producto.filter(categoria=categoria)
                if not costos_categoria.exists():
                    continue  # Saltar si no hay costos para esta categoría

                # Inicializar los datos para la categoría actual
                datos_categoria = {
                    "costos_mensuales": {},
                    "totales_anuales": {}
                }

                # Obtener el costo de la categoría para usar como referencia
                costo_categoria = costos_categoria.first().costo

                # Agregar la referencia con el costo de la categoría
                datos_categoria["referencia"] = float(costo_categoria)

                # Repetir el costo mensual durante 5 años y calcular los totales anuales como promedio
                for anio in range(1, 6):
                    suma_anual = 0
                    datos_categoria["costos_mensuales"][f"Año {anio}"] = {}
                    for mes in range(1, 13):
                        referencia_mes = f"Año {anio} - Mes {mes}"
                        # Usar el costo de la categoría para todos los meses del año
                        costo_mensual = float(costo_categoria)

                        # Asignar el costo mensual
                        datos_categoria["costos_mensuales"][f"Año {anio}"][str(mes)] = costo_mensual
                        suma_anual += costo_mensual

                    # Calcular el total anual como el promedio mensual de los 12 meses
                    total_anual = suma_anual / 12 if suma_anual > 0 else 0
                    datos_categoria["totales_anuales"][f"Año {anio}"] = total_anual

                # Agregar la categoría con sus costos al producto
                datos_producto[categoria.nombre] = datos_categoria

            # Agregar el producto con sus categorías al reporte final
            reporte_costos[producto.nombre] = datos_producto

        # Retornar el JSON estructurado
        return Response({"resultado": reporte_costos}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
