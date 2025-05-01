from django.urls import path
from inventario.views.material_views import agregar_material, listar_materiales
from inventario.views.venta_views import buscar_materiales

urlpatterns = [
    path('agregar/', agregar_material, name='agregar_material'),
    path('listar/', listar_materiales, name='listar_materiales'),
    path('api/materiales/', buscar_materiales, name='buscar_materiales'),
]
