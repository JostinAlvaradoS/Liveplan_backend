# urls.py
from django.urls import path
from .views import create_plan_negocio, create_inversion_inicial, create_detalle_inversion_inicial, \
    get_plan_negocio_by_autor, get_inversion_inicial_by_plan_negocio

urlpatterns = [
    path('plan-negocio/', create_plan_negocio, name='create-plan-negocio'),
    path('inversion-inicial/', create_inversion_inicial, name='create-inversion-inicial'),
    path('detalle-inversion-inicial/', create_detalle_inversion_inicial, name='create-detalle-inversion-inicial'),
    path('get-plan-negocio/', get_plan_negocio_by_autor, name='get_plan_negocio_by_autor'),
    path('get-inversion-inicial/', get_inversion_inicial_by_plan_negocio, name='get_inversion_inicial_by_plan_negocio'),
]
