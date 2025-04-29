from django.urls import path
from inventario.views.proveedor_views import agregar_proveedor, listar_proveedores

urlpatterns = [
    path('agregar/', agregar_proveedor, name='agregar_proveedor'),
    path('listar/', listar_proveedores, name='listar_proveedores'),
]
