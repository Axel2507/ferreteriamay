from django.urls import path
from inventario.views.categoria_views import agregar_categoria, listar_categorias, actualizar_categoria,eliminar_categoria,activar_categoria,desactivar_categoria

urlpatterns = [
    path('agregar/', agregar_categoria, name='agregar_categoria'),
    path('listar/', listar_categorias, name='listar_categorias'),
    path('actualizar/<str:id>/', actualizar_categoria, name='actualizar_categoria'),
    path('eliminar/<int:id>/', eliminar_categoria, name='eliminar_categoria'),
    path('activar/<int:id>/', activar_categoria, name='activar_categoria'),
    path('desactivar/<str:id>/', desactivar_categoria, name='desactivar_categoria')

]