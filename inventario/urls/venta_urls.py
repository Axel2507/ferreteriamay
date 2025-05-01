from django.urls import path
from inventario.views.venta_views import agregar_venta

urlpatterns = [
    path("agregar/", agregar_venta, name="agregar_venta"),

]