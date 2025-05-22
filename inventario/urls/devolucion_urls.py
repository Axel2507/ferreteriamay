from django.urls import path
from inventario.views.devolucion_views import (
    agregar_devolucion,
    listar_devoluciones,
    buscar_venta,
    seleccionar_venta,
    procesar_devolucion,
    ver_devolucion # esta vista faltaba en tu urls.py
)

urlpatterns = [
    path('agregar/', agregar_devolucion, name='agregar_devolucion'),
    path('listar/', listar_devoluciones, name='listar_devoluciones'),
    path('buscar-venta/', buscar_venta, name='buscar_venta'),
    path('seleccionar-venta/<int:venta_id>/', seleccionar_venta, name='seleccionar_venta'),
    path('devolucion/procesar/', procesar_devolucion, name='procesar_devolucion'),
    path('ver/<int:devolucion_id>/', ver_devolucion, name='ver_devolucion') # detalle de devolución
]