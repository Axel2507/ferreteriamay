from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BarcodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("📡 Cliente WebSocket conectado")  # ← este mensaje aparecerá en el log del servidor
        await self.accept()

    async def disconnect(self, close_code):
        print("❌ Cliente desconectado del WebSocket")

    async def receive(self, text_data):
        print("📦 Dato recibido:", text_data)
        data = json.loads(text_data)
        barcode = data.get("barcode")
        # Enviar el código al navegador conectado (eco)
        await self.send(json.dumps({"barcode": barcode}))