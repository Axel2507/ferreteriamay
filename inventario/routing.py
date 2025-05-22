# inventario/routing.py
from django.urls import re_path
from inventario.consumers import BarcodeConsumer

websocket_urlpatterns = [
    re_path(r'^ws/barcodes/$', BarcodeConsumer.as_asgi()),
]
