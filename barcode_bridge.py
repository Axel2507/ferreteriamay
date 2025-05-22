import serial
import asyncio
import websockets
import json

SERIAL_PORT = 'COM4'  # ← Cambia según tu puerto
BAUD_RATE = 9600
WS_URI = "wss://TUDOMINIO/ws/barcode/"

async def serial_to_ws():
    async with websockets.connect(WS_URI) as ws:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    await ws.send(json.dumps({"barcode": line}))
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(serial_to_ws())
