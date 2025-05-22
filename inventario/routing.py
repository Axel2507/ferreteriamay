# inventario/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^wss/barcodes/$',consumers.BarcodeConsumer.as_asgi()),
]
