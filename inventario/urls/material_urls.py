from django.urls import path
from inventario.views.material_views import agregar_material

urlpatterns = [
    path('agregar/', agregar_material, name='agregar_material'),
]
