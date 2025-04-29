from django.urls import path
from inventario.views.unidad_views import agregar_unidad, listar_unidades

urlpatterns = [
    path('agregar/', agregar_unidad, name='agregar_unidad'),
    path('listar/',listar_unidades, name='listar_unidades'),
]
