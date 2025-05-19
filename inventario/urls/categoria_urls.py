from django.urls import path
from inventario.views.categoria_views import agregar_categoria, listar_categorias, actualizar_categoria

urlpatterns = [
    path('agregar/', agregar_categoria, name='agregar_categoria'),
    path('listar/', listar_categorias, name='listar_categorias'),
    path('actualizar/<str:id>/', actualizar_categoria, name='actualizar_categoria'),
]