from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BarcodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("barcode_group", self.channel_name)
        await self.accept()
        print("🔌 Cliente conectado")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("barcode_group", self.channel_name)
        print("❌ Cliente desconectado")

    async def receive(self, text_data):
        print("📦 Datos recibidos:", text_data)
        data = json.loads(text_data)
        barcode = data.get("barcode")
        if barcode:
            # reenviar el código a todos los clientes conectados
            await self.channel_layer.group_send(
                "barcode_group",
                {
                    "type": "barcode_message",
                    "barcode": barcode
                }
            )

    async def barcode_message(self, event):
        barcode = event["barcode"]
        print("📤 Reenviando a navegadores:", barcode)
        await self.send(text_data=json.dumps({
            "barcode": barcode
        }))
