from django.urls import path
from inventario.views.venta_views import agregar_venta, ticket_venta

urlpatterns = [
    path("agregar/", agregar_venta, name="agregar_venta"),
    path('<int:venta_id>/ticket/', ticket_venta, name='ticket_venta'),
]

