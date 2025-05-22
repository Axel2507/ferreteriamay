from django.urls import path
from inventario.views.descuento_views import aplicar_descuento, listar_descuentos

urlpatterns = [
    path('aplicar/', aplicar_descuento, name='aplicar_descuento'),
    path('listar/', listar_descuentos, name='listar_descuentos'),
]