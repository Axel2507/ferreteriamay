from django.urls import path
from inventario.views.proveedor_views import agregar_proveedor, listar_proveedores,actualizar_proveedor

urlpatterns = [
    path('agregar/', agregar_proveedor, name='agregar_proveedor'),
    path('listar/', listar_proveedores, name='listar_proveedores'),
    path('actualizar/<int:id>/', actualizar_proveedor, name='actualizar_proveedor')
]
