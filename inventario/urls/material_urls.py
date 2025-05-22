from django.urls import path
from inventario.views.material_views import agregar_material, listar_materiales, actualizar_material,desactivar_material
from inventario.views.venta_views import buscar_materiales

urlpatterns = [
    path('agregar/', agregar_material, name='agregar_material'),
    path('listar/', listar_materiales, name='listar_materiales'),
    path('actualizar/<str:codigo>/', actualizar_material, name='actualizar_material'),
    path('materiales/<str:codigo>/desactivar/', desactivar_material, name='desactivar_material')
]