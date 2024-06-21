# urls.py
from django.urls import path
from .views import create_plan_negocio, create_inversion_inicial, create_detalle_inversion_inicial

urlpatterns = [
    path('plan-negocio/', create_plan_negocio, name='create-plan-negocio'),
    path('inversion-inicial/', create_inversion_inicial, name='create-inversion-inicial'),
    path('detalle-inversion-inicial/', create_detalle_inversion_inicial, name='create-detalle-inversion-inicial'),
]
