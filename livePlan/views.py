from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from django.db.models import Sum
from livePlan.auxiliares import calcular_ventas_mensuales
from .models import Categorias_costos, ComposicionFinanciamiento, Costo, IndicadoresMacro, PrecioVenta, Producto_servicio, VariacionAnual, VentaDiaria, costosVenta, depreciacionMensual, gastosOperacion, planNegocio, inversionInicial, detalleInversionInicial, prestamo, proyeccionVentas, ventasMes
from .serializers import CostoSerializer, FinanciamientoSerializer, IndicadoresMacroSerializer, PlanNegocioSerializer, InversionInicialSerializer, DetalleInversionInicialSerializer, PrecioVentaSerializer, ProductoServicioSerializer, SupuestoSerializer, VariacionAnualSerializer, VentaDiariaSerializer

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
                'tipo':inversion.tipo.id,
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
def create_financiamiento(request):
    if request.method == 'POST':
        serializer = FinanciamientoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

                 # Guardar los totales anuales en la tabla ventasMes
                ventas_mes, created = ventasMes.objects.update_or_create(
                        planNegocio=plan,
                        producto=producto,
                        defaults={
                            'anio1': totales_anuales.get('Año 1'),
                            'anio2': totales_anuales.get('Año 2'),
                            'anio3': totales_anuales.get('Año 3'),
                            'anio4': totales_anuales.get('Año 4'),
                            'anio5': totales_anuales.get('Año 5'),
                        }
                    )
            
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


from django.db.models import Sum

@api_view(['POST'])
def calcular_volumenxmes(request):
    try:
        # Obtener el ID del plan de negocio del cuerpo de la solicitud POST
        plan_negocio_id = request.data.get('planNegocio')
        
        # Verificar si se proporcionó el ID
        if not plan_negocio_id:
            return Response({"error": "El ID del plan de negocio es requerido."}, status=400)

        # Verificar que el plan de negocio existe
        plan = planNegocio.objects.get(id=plan_negocio_id)
        
        productos = Producto_servicio.objects.filter(planNegocio=plan)
        resultados = {"resultado": {}}
        
        # Para cada producto/servicio
        for producto in productos:
            try:
                # Obtener los costos asociados a este producto/servicio
                costos = Costo.objects.filter(planNegocio=plan, producto_servicio=producto).aggregate(total_costo=Sum('costo'))
                total_costo_producto = costos['total_costo'] if costos['total_costo'] else 0

                if total_costo_producto == 0:
                    resultados["resultado"][producto.nombre] = {"error": "No se encontraron costos asociados a este producto."}
                    continue

                # Obtener las ventas anuales del producto desde ventasMes
                ventas = ventasMes.objects.filter(planNegocio=plan, producto=producto).first()
                
                if not ventas:
                    resultados["resultado"][producto.nombre] = {"error": "No se encontraron ventas para este producto."}
                    continue

                # Inicializar el resultado de las ganancias mensuales y anuales por año
                ganancia_mensual = {f"Año {anio}": {str(mes): 0 for mes in range(1, 13)} for anio in range(1, 6)}
                totales_anuales = {f"Año {anio}": 0 for anio in range(1, 6)}
                
                # Para cada año, obtener el total anual de ventas y distribuirlo entre los 12 meses
                for anio in range(1, 6):
                    total_anio = getattr(ventas, f'anio{anio}', 0)  # Obtener el valor del año respectivo
                    if total_anio:
                        total_anio_mensual = total_anio / 12  # Distribuir el total anual entre los 12 meses
                        
                        # Calcular la ganancia mensual y el total anual para cada mes
                        for mes in range(1, 13):
                            ganancia_mensual[f"Año {anio}"][str(mes)] = total_anio_mensual * total_costo_producto
                            totales_anuales[f"Año {anio}"] += ganancia_mensual[f"Año {anio}"][str(mes)]

                # Verificar si ya existe un registro en costosVenta para este planNegocio y producto
                costos_venta_existente = costosVenta.objects.filter(planNegocio=plan, producto=producto).first()
                
                if not costos_venta_existente:
                    # Crear un nuevo registro si no existe
                    costos_venta = costosVenta.objects.create(
                        planNegocio=plan,
                        producto=producto,
                        anio1=totales_anuales["Año 1"],
                        anio2=totales_anuales["Año 2"],
                        anio3=totales_anuales["Año 3"],
                        anio4=totales_anuales["Año 4"],
                        anio5=totales_anuales["Año 5"]
                    )
                    costos_venta.save()
                else:
                    # Si ya existe, actualizar los valores de los totales anuales
                    costos_venta_existente.anio1 = totales_anuales["Año 1"]
                    costos_venta_existente.anio2 = totales_anuales["Año 2"]
                    costos_venta_existente.anio3 = totales_anuales["Año 3"]
                    costos_venta_existente.anio4 = totales_anuales["Año 4"]
                    costos_venta_existente.anio5 = totales_anuales["Año 5"]
                    costos_venta_existente.save()

                # Agregar los resultados al JSON de respuesta
                resultados["resultado"][producto.nombre] = {
                    "ganancia_mensual": ganancia_mensual,
                    "totales_anuales": totales_anuales
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
def calcular_costoMateriaPrima(request):
    try:
        # Obtener el ID del plan de negocio del cuerpo de la solicitud POST
        plan_negocio_id = request.data.get('planNegocio')
        
        # Verificar si se proporcionó el ID
        if not plan_negocio_id:
            return Response({"error": "El ID del plan de negocio es requerido."}, status=400)

        # Verificar que el plan de negocio existe
        plan = planNegocio.objects.get(id=plan_negocio_id)
        
        productos = Producto_servicio.objects.filter(planNegocio=plan)
        resultados = {"resultado": {}}
        
        # Filtrar los costos con la categoría ID=2
        tipo2_categoria_id = 2
        
        # Para cada producto/servicio
        for producto in productos:
            try:
                # Obtener los costos de tipo2 asociados a este producto/servicio
                costos_tipo2 = Costo.objects.filter(planNegocio=plan, producto_servicio=producto, categoria_id=tipo2_categoria_id).aggregate(total_costo_tipo2=Sum('costo'))
                total_costo_tipo2_producto = costos_tipo2['total_costo_tipo2'] if costos_tipo2['total_costo_tipo2'] else 0

                if total_costo_tipo2_producto == 0:
                    resultados["resultado"][producto.nombre] = {"error": "No se encontraron costos de tipo2 asociados a este producto."}
                    continue

                # Obtener las ventas anuales del producto desde ventasMes
                ventas = ventasMes.objects.filter(planNegocio=plan, producto=producto).first()
                
                if not ventas:
                    resultados["resultado"][producto.nombre] = {"error": "No se encontraron ventas para este producto."}
                    continue

                # Inicializar el resultado de las ganancias mensuales y anuales por año
                ganancia_mensual = {f"Año {anio}": {str(mes): 0 for mes in range(1, 13)} for anio in range(1, 6)}
                totales_anuales = {f"Año {anio}": 0 for anio in range(1, 6)}
                
                # Para cada año, obtener el total anual de ventas y distribuirlo entre los 12 meses
                for anio in range(1, 6):
                    total_anio = getattr(ventas, f'anio{anio}', 0)  # Obtener el valor del año respectivo
                    if total_anio:
                        total_anio_mensual = total_anio / 12  # Distribuir el total anual entre los 12 meses
                        
                        # Calcular la ganancia mensual y el total anual para cada mes
                        for mes in range(1, 13):
                            ganancia_mensual[f"Año {anio}"][str(mes)] = total_anio_mensual * total_costo_tipo2_producto
                            totales_anuales[f"Año {anio}"] += ganancia_mensual[f"Año {anio}"][str(mes)]

                # Agregar los resultados al JSON de respuesta
                resultados["resultado"][producto.nombre] = {
                    "ganancia_mensual": ganancia_mensual,
                    "totales_anuales": totales_anuales
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
def calcular_gastos_operacion(request):
    try:
        # Verificar que el planNegocio esté presente en la solicitud
        plan_negocio = request.data.get('planNegocio')
        if not plan_negocio:
            return Response({"error": "El campo 'planNegocio' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener todos los registros de gastosOperacion
        gastos = gastosOperacion.objects.all()

        if not gastos:
            return Response({"error": "No se encontraron registros de gastos de operación."}, status=status.HTTP_404_NOT_FOUND)
        
        resultados = {"resultado": {}}
        num_anios = 5  # Número de años

        # Para cada gasto de operación
        for gasto in gastos:
            try:
                referencia = gasto.referencia
                
                if referencia is None:
                    resultados["resultado"][gasto.nombre] = {"error": "La referencia no está definida para este gasto."}
                    continue

                # Inicializar los valores mensuales por año
                gastos_mensuales_totales = {f"Año {anio+1}": {str(mes): float(referencia) for mes in range(1, 13)} for anio in range(num_anios)}
                
                # Calcular el total anual para cada año
                totales_anuales = {anio: sum(gastos_mensuales_totales[anio][str(mes)] for mes in range(1, 13)) for anio in gastos_mensuales_totales}

                # Agregar los resultados para cada gasto de operación
                resultados["resultado"][gasto.nombre] = {
                    "gastos_mensuales": gastos_mensuales_totales,
                    "totales_anuales": totales_anuales,
                }

            except Exception as e:
                # Manejar cualquier excepción durante el procesamiento
                resultados["resultado"][gasto.nombre] = {"error": str(e)}

        return Response(resultados)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generar_reporte_montoInteres(request):
    try:
        # Obtener el planNegocio del cuerpo de la solicitud
        plan_negocio = request.data.get('planNegocio')
        if not plan_negocio:
            return Response({"error": "El campo 'planNegocio' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Sumar todos los importes de la tabla inversionInicial según el planNegocio
        suma_importes = inversionInicial.objects.filter(planNegocio_id=plan_negocio).aggregate(total_importe=Sum('importe'))['total_importe']

        if suma_importes is None:
            return Response({"error": "No se encontraron importes para el plan de negocio proporcionado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el valor de deuda desde la tabla financiamientoInversiones según el planNegocio
        financiamiento = ComposicionFinanciamiento.objects.filter(planNegocio_id=plan_negocio).first()
        if not financiamiento or financiamiento.deuda is None:
            return Response({"error": "No se encontró financiamiento o el campo 'deuda' no está definido para el plan de negocio proporcionado."}, 
                            status=status.HTTP_404_NOT_FOUND)

        deuda = financiamiento.deuda

        # Obtener la tasa de interés de deuda desde la tabla indicadoresMacro según el planNegocio
        indicadores = IndicadoresMacro.objects.filter(planNegocio_id=plan_negocio).first()
        if not indicadores or indicadores.tasaInteresDeuda is None:
            return Response({"error": "No se encontraron indicadores o el campo 'tasaInteresDeuda' no está definido para el plan de negocio proporcionado."}, 
                            status=status.HTTP_404_NOT_FOUND)

        tasa_interes_deuda = indicadores.tasaInteresDeuda

        # Calcular el resultado solicitado: (suma_importes * deuda / 100)
        resultado_prestamo = (suma_importes * deuda) / 100

        # Preparar la respuesta
        resultado = {
            "tasa_interes_deuda": tasa_interes_deuda,
            "resultado_prestamo": resultado_prestamo
        }

        return Response({"resultado": resultado}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

from decimal import Decimal


@api_view(['POST'])
def gestionar_prestamo(request):
    try:
        plan_negocio_id = request.data.get('planNegocio')
        if not plan_negocio_id:
            return Response({"error": "El campo 'planNegocio' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar existencia del plan de negocio
        try:
            plan_negocio = planNegocio.objects.get(id=plan_negocio_id)
        except planNegocio.DoesNotExist:
            return Response({"error": "El plan de negocio no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si ya existe un préstamo para el plan de negocio
        prestamo_existente = prestamo.objects.filter(planNegocio=plan_negocio).first()

        if not prestamo_existente:
            prestamo_existente = prestamo(planNegocio=plan_negocio)

        # Actualizar campos del préstamo si están presentes en la solicitud
        if 'periodoCapitalizacion' in request.data and request.data['periodoCapitalizacion'] is not None:
            prestamo_existente.periodoCapitalizacion = request.data['periodoCapitalizacion']
        
        if 'tasaInteresMensual' in request.data and request.data['tasaInteresMensual'] is not None:
            prestamo_existente.tasaInteresMensual = request.data['tasaInteresMensual']
        
        if 'periodosAmortizacion' in request.data and request.data['periodosAmortizacion'] is not None:
            prestamo_existente.periodosAmortizacion = request.data['periodosAmortizacion']

        prestamo_existente.save()

        # Verificar que todos los datos necesarios están presentes para el cálculo
        if (prestamo_existente.periodoCapitalizacion is not None and
            prestamo_existente.tasaInteresMensual is not None and
            prestamo_existente.periodosAmortizacion is not None):
            
            # Obtener el monto total de inversión y deuda
            inversiones = inversionInicial.objects.filter(planNegocio=plan_negocio).aggregate(total_importes=Sum('importe'))['total_importes']
            deuda_porcentaje = ComposicionFinanciamiento.objects.get(planNegocio=plan_negocio).deuda / Decimal(100)
            tasa_anual = IndicadoresMacro.objects.filter(planNegocio_id=plan_negocio).first()
            tasa_anual = tasa_anual.tasaInteresDeuda/100
            monto_total_deuda = Decimal(inversiones) * deuda_porcentaje

            tasa_interes_mensual = Decimal(prestamo_existente.tasaInteresMensual) / Decimal(100)
            periodos_amortizacion = Decimal(prestamo_existente.periodosAmortizacion)
            
            # Cálculo de cuota fija mensual (corrección de tipos float y Decimal)
            if tasa_interes_mensual > 0:
                cuota_fija_mensual = monto_total_deuda * (tasa_anual / prestamo_existente.periodoCapitalizacion) / (1 - (1 + (tasa_anual / prestamo_existente.periodoCapitalizacion)) ** -periodos_amortizacion)
            else:
                cuota_fija_mensual = monto_total_deuda / periodos_amortizacion

            prestamo_existente.cuotaFijaMensual = cuota_fija_mensual
            prestamo_existente.save()

            # Generar reporte mensual
            reporte_mensual = []
            saldo_inicial = monto_total_deuda
            for mes in range(1, 61):
                intereses = saldo_inicial * tasa_interes_mensual
                abono_capital = cuota_fija_mensual - intereses
                saldo_final = saldo_inicial - abono_capital

                reporte_mensual.append({
                    "Mes": mes,
                    "Saldo Inicial": saldo_inicial,
                    "Intereses": intereses,
                    "Abono Capital": abono_capital,
                    "Saldo Final": saldo_final
                })

                saldo_inicial = saldo_final

            # Agrupar reporte mensual por año
            reporte_anual = {}
            for anio in range(1, 6):
                reporte_anual[f"Año {anio}"] = [reporte_mensual[mes - 1] for mes in range((anio - 1) * 12 + 1, anio * 12 + 1)]

            return Response({
                "reporte_anual": reporte_anual,
                "tasaInteresMensual": prestamo_existente.tasaInteresMensual,
                "cuotaFijaMensual": cuota_fija_mensual,
                "periodoCapitalizacion": prestamo_existente.periodoCapitalizacion,
                "periodosAmortizacion": prestamo_existente.periodosAmortizacion
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "periodoCapitalizacion": prestamo_existente.periodoCapitalizacion,
                "tasaInteresMensual": prestamo_existente.tasaInteresMensual,
                "periodosAmortizacion": prestamo_existente.periodosAmortizacion,
                "cuotaFijaMensual": prestamo_existente.cuotaFijaMensual,
                "message": "Datos faltantes para realizar el cálculo de préstamo. Algunos valores son null."
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generar_utilidad_bruta(request):
    try:
        # Obtener el ID del plan de negocio desde el POST
        plan_negocio_id = request.data.get('planNegocio')
        if not plan_negocio_id:
            return Response({"error": "El campo 'planNegocio' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar la existencia del plan de negocio
        plan_negocio = planNegocio.objects.get(id=plan_negocio_id)

        # Inicializar el diccionario para almacenar el detalle anual
        ventas_mensuales_detalladas = {}

        # Obtener todos los productos asociados a este plan de negocio
        productos = Producto_servicio.objects.filter(planNegocio=plan_negocio)

        # Obtener el valor total de gastos de operación
        total_gastos_operacion = gastosOperacion.objects.all().aggregate(total=Sum('referencia'))['total'] or Decimal(0)

        # Cargar en memoria los precios de venta, proyecciones y costos de ventas
        precios_venta = {p.producto_servicio.id: Decimal(p.precio) for p in PrecioVenta.objects.filter(planNegocio=plan_negocio)}
        proyecciones_ventas = {
            (v.producto.id, f'anio{anio}'): Decimal(getattr(v, f'anio{anio}', 0))
            for v in ventasMes.objects.filter(planNegocio=plan_negocio)
            for anio in range(1, 6)
        }
        costos_ventas = {
            (c.producto.id, f'anio{anio}'): Decimal(getattr(c, f'anio{anio}', 0)) / Decimal(12)
            for c in costosVenta.objects.filter(planNegocio=plan_negocio)
            for anio in range(1, 6)
        }

        # Obtener las depreciaciones mensuales
        depreciaciones_mensuales = {
            d.inversion.id: Decimal(d.depreciacionMensual)
            for d in depreciacionMensual.objects.filter(planNegocio=plan_negocio, inversion__tipo=1)
        }

        # Obtener las amortizaciones mensuales
        amortizaciones_mensuales = {
            a.inversion.id: Decimal(a.depreciacionMensual)
            for a in depreciacionMensual.objects.filter(planNegocio=plan_negocio, inversion__tipo=2)
        }

        # Iterar por cada año (anio1 a anio5)
        for anio in range(1, 6):
            ventas_mensuales = {}
            total_ventas_anio = Decimal(0)
            total_costos_anio = Decimal(0)
            total_utilidad_bruta_anio = Decimal(0)
            total_depreciaciones_anio = Decimal(0)
            total_amortizaciones_anio = Decimal(0)
            total_utilidad_previo_interes_impuestos_anio = Decimal(0)

            # Iterar por cada mes (1 a 12)
            for mes in range(1, 13):
                total_ventas_mes = Decimal(0)
                total_costos_mes = Decimal(0)
                total_depreciaciones_mes = Decimal(0)
                total_amortizaciones_mes = Decimal(0)

                # Iterar sobre los productos para calcular las ventas y costos por mes
                for producto in productos:
                    producto_id = producto.id

                    # Obtener el precio de venta del producto
                    precio_venta = precios_venta.get(producto_id)
                    if precio_venta is None:
                        continue  # Saltar si no hay precio de venta definido para el producto

                    # Obtener las ventas anuales del año actual
                    ventas_anio = proyecciones_ventas.get((producto_id, f'anio{anio}'), Decimal(0))
                    if ventas_anio == 0:
                        continue  # Saltar si no hay ventas para ese año

                    # Calcular las ventas mensuales ajustadas (ventas anuales / 12)
                    ventas_mes_ajustadas = ventas_anio / Decimal(12)
                    ventas_producto_mes = ventas_mes_ajustadas * precio_venta
                    total_ventas_mes += ventas_producto_mes

                    # Obtener el costo de ventas mensual del año actual
                    costo_ventas_mes = costos_ventas.get((producto_id, f'anio{anio}'), Decimal(0))
                    total_costos_mes += costo_ventas_mes

                # Calcular las depreciaciones mensuales
                for inversion_id, depreciacion in depreciaciones_mensuales.items():
                    total_depreciaciones_mes += depreciacion

                # Calcular las amortizaciones mensuales
                for inversion_id, amortizacion in amortizaciones_mensuales.items():
                    total_amortizaciones_mes += amortizacion

                # Calcular y almacenar ventas, costos, utilidad bruta, gastos operativos, depreciaciones y amortizaciones
                ventas_mensuales[f"VentasMes{mes}"] = round(total_ventas_mes, 2)
                ventas_mensuales[f"CostoVentasMes{mes}"] = round(total_costos_mes, 2)
                ventas_mensuales[f"UtilidadBrutaMes{mes}"] = round(total_ventas_mes - total_costos_mes, 2)
                ventas_mensuales[f"GastosOperacionMes{mes}"] = round(total_gastos_operacion, 2)  # Gastos operativos mensual
                ventas_mensuales[f"DepreciacionesMes{mes}"] = round(total_depreciaciones_mes, 2)
                ventas_mensuales[f"AmortizacionesMes{mes}"] = round(total_amortizaciones_mes, 2)
                ventas_mensuales[f"UtilidadPrevioInteresImpuestosMes{mes}"] = round(
                    total_ventas_mes - total_costos_mes - total_gastos_operacion - total_depreciaciones_mes - total_amortizaciones_mes, 2)

                # Acumular ventas, costos, utilidad bruta, depreciaciones y amortizaciones en el total anual
                total_ventas_anio += total_ventas_mes
                total_costos_anio += total_costos_mes
                total_utilidad_bruta_anio += (total_ventas_mes - total_costos_mes)
                total_depreciaciones_anio += total_depreciaciones_mes
                total_amortizaciones_anio += total_amortizaciones_mes
                total_utilidad_previo_interes_impuestos_anio += (total_ventas_mes - total_costos_mes - total_gastos_operacion - total_depreciaciones_mes - total_amortizaciones_mes)

            # Calcular y almacenar totales anuales
            utilidad_bruta_anio = total_ventas_anio - total_costos_anio
            ventas_mensuales["TotalVentasAnio"] = round(total_ventas_anio, 2)
            ventas_mensuales["CostoVentasAnio"] = round(total_costos_anio, 2)
            ventas_mensuales["UtilidadBrutaAnio"] = round(utilidad_bruta_anio, 2)
            ventas_mensuales["CostoGastosOperacionAnio"] = round(total_gastos_operacion * 12, 2)  # Gastos operativos anuales
            ventas_mensuales["DepreciacionesAnio"] = round(total_depreciaciones_anio, 2)
            ventas_mensuales["AmortizacionesAnio"] = round(total_amortizaciones_anio, 2)
            ventas_mensuales["UtilidadPrevioInteresImpuestosAnio"] = round(total_utilidad_previo_interes_impuestos_anio, 2)

            ventas_mensuales_detalladas[f"Anio{anio}"] = ventas_mensuales

        # Respuesta JSON con los detalles de ventas mensuales, costos y utilidades
        return Response({
            "plan_negocio": plan_negocio.descripcion,
            "ventas_mensuales_anuales": ventas_mensuales_detalladas
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

