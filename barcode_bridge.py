import serial
import asyncio
import websockets
import json
import ssl

SERIAL_PORT = 'COM4'  # Cambia si tu Arduino usa otro puerto
BAUD_RATE = 9600
WS_URI = "wss://ferremay.com/ws/barcodes/"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Solo para pruebas. En producción usa CERT_REQUIRED

async def serial_to_ws():
    async with websockets.connect(WS_URI, ssl=ssl_context) as ws:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    if line.startswith("Código escaneado:"):
                        barcode = line.replace("Código escaneado:", "").strip()
                    else:
                        barcode = line
                    await ws.send(json.dumps({"barcode": barcode}))
            await asyncio.sleep(0.1)
            
if __name__ == "__main__":
    asyncio.run(serial_to_ws())
