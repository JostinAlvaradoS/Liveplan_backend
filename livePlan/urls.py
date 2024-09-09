# urls.py
from django.urls import path
from .views import calcular_ventas, create_costos, create_indicadores_macro, create_plan_negocio, create_inversion_inicial, create_detalle_inversion_inicial, create_precios, create_producto_servicio, create_supuesto, create_variacion_anual, create_venta_diaria, generar_reporte_costos, generar_tabla_precios, gestionar_depreciacion_mensual, \
    get_plan_negocio_by_autor, get_inversion_inicial_by_plan_negocio, obtener_proyeccion_demanda, update_vida_util

urlpatterns = [
    path('plan-negocio/', create_plan_negocio, name='create-plan-negocio'),
    path('inversion-inicial/', create_inversion_inicial, name='create-inversion-inicial'),
    path('detalle-inversion-inicial/', create_detalle_inversion_inicial, name='create-detalle-inversion-inicial'),
    path('get-plan-negocio/', get_plan_negocio_by_autor, name='get_plan_negocio_by_autor'),
    path('get-inversion-inicial/', get_inversion_inicial_by_plan_negocio, name='get_inversion_inicial_by_plan_negocio'),
    path('create_supuesto/', create_supuesto, name='create_supuesto'),
    path('create_venta_diaria/', create_venta_diaria, name='create_venta_diaria'),
    path('create_variacion_anual/', create_variacion_anual, name='create_variacion_anual'),
    path('create_producto_servicio/', create_producto_servicio, name='create_variacion_anual'),
    path('create_precios/', create_precios, name='create_variacion_anual'),
    path('create_costos/', create_costos, name='create_variacion_anual'),
    path('get_proyeccion_demanda/', obtener_proyeccion_demanda, name='create_variacion_anual'),
    path('create_indicadores_macro/', create_indicadores_macro),
    path('calcular_ventas/', calcular_ventas),
    path('update_vida_util/', update_vida_util),
    path('gestionar_depreciacion_mensual/', gestionar_depreciacion_mensual),
    path('generar_tabla_precios/', generar_tabla_precios),
     path('generar_reporte_costos/', generar_reporte_costos),
]
