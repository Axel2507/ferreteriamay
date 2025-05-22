from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BarcodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        barcode = data.get("barcode")
        # Enviar el código al navegador conectado (eco)
        await self.send(json.dumps({"barcode": barcode}))