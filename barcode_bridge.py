import serial
import asyncio
import websockets
import json
import ssl

SERIAL_PORT = 'COM4'  # ← Cambia según tu puerto
BAUD_RATE = 9600
WS_URI = "wss://ec2-3-87-2-50.compute-1.amazonaws.com:9000/wss/barcodes/"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

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
