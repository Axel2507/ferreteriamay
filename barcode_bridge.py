import serial
import threading
import time
from flask import Flask, jsonify # jsonify podría no ser necesario si solo usas WebSockets
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import eventlet # Importar eventlet

eventlet.monkey_patch() # Es importante para que las operaciones de red sean no bloqueantes

# --- Configuración ---
SERIAL_PORT = 'COM4'  # ¡¡¡IMPORTANTE!!! Revisa que sea el puerto correcto
BAUD_RATE = 9600
HTTP_HOST = '127.0.0.1'
HTTP_PORT = 5001
# --------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_secreta!' # Necesario para SocketIO
CORS(app, resources={r"/*": {"origins": "*"}}) # Permite CORS para SocketIO también

# Configura SocketIO. Usa async_mode='eventlet'.
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Variable global para almacenar el último código de barras escaneado
last_barcode_scanned = ""
# No necesitamos un Lock explícito aquí si la actualización y emisión se hacen desde un solo hilo (el de serial)
# o si las operaciones de SocketIO son seguras para hilos (generalmente lo son para emit).

def read_from_serial():
    """
    Lee datos del puerto serie en un hilo separado y emite
    el nuevo código de barras a través de WebSockets.
    También actualiza la variable global last_barcode_scanned.
    """
    global last_barcode_scanned
    ser = None
    while True:
        try:
            if ser is None or not ser.is_open:
                print(f"Intentando conectar al puerto serie: {SERIAL_PORT} a {BAUD_RATE} baudios...")
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                print(f"Conectado a {SERIAL_PORT}. Esperando códigos de barras...")
                # Al (re)conectar, si ya había un código, se podría emitir
                # if last_barcode_scanned:
                #    socketio.emit('last_known_barcode', {'barcode': last_barcode_scanned})


            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                if line:
                    prefix = "Código escaneado: " # Asegúrate que tu Arduino aún envía este prefijo
                    barcode_data = ""
                    if line.startswith(prefix):
                        barcode_data = line[len(prefix):]
                    else:
                        # Si no tiene el prefijo, podrías decidir usar la línea completa
                        # o ignorarla si esperas un formato específico.
                        # Por ahora, asumamos que si no tiene prefijo, podría ser un código directo.
                        barcode_data = line 
                        print(f"Línea recibida sin prefijo esperado, usando como código: {line}")


                    if barcode_data: # Solo procesar si tenemos datos de código de barras
                        last_barcode_scanned = barcode_data
                        print(f"Nuevo código de barras detectado: {barcode_data}. Emitiendo por WebSocket.")
                        # Emitir el nuevo código de barras a todos los clientes conectados
                        socketio.emit('nuevo_codigo_barra', {'barcode': barcode_data})

            # Pausa breve para no sobrecargar la CPU y permitir que SocketIO procese eventos
            socketio.sleep(0.01) # Usar socketio.sleep en lugar de time.sleep en hilos gestionados por eventlet/gevent

        except serial.SerialException as e:
            print(f"Error de puerto serie: {e}")
            if ser and ser.is_open:
                ser.close()
            ser = None # Asegura que se intente reconectar
            print("Intentando reconectar en 5 segundos...")
            time.sleep(5) # time.sleep está bien aquí porque estamos fuera del bucle principal de eventlet
        except Exception as e:
            print(f"Error inesperado en read_from_serial: {e}")
            if ser and ser.is_open:
                ser.close()
            ser = None
            time.sleep(5)

@socketio.on('connect')
def handle_connect():
    """
    Cuando un nuevo cliente se conecta, se le puede enviar el último código
    de barras conocido (si existe y si se desea esta funcionalidad).
    """
    client_sid = threading.get_ident() # O alguna forma de identificar al cliente si es necesario
    print(f"Cliente conectado: {client_sid}")
    if last_barcode_scanned:
        # Emitir solo al cliente que se acaba de conectar (usando request.sid si estás en el contexto de una request)
        # Sin embargo, emitir a todos no es malo, el cliente puede decidir si ya lo tiene.
        # O, para más precisión, necesitarías el sid del cliente, que se obtiene en el contexto del evento.
        # emit('last_known_barcode', {'barcode': last_barcode_scanned}, room=request.sid)
        # Por simplicidad, el cliente al conectarse puede pedirlo o simplemente esperar nuevos códigos.
        # O podemos enviarles un evento general "estado_actual"
        emit('last_known_barcode', {'barcode': last_barcode_scanned}) 
        print(f"Enviando último código conocido '{last_barcode_scanned}' al nuevo cliente.")


@app.route('/status') # Ruta HTTP tradicional para verificar estado (opcional)
def status():
    return jsonify({"status": "Servidor puente de código de barras (WebSocket) activo", "last_barcode": last_barcode_scanned})

if __name__ == '__main__':
    # Iniciar el hilo para leer desde el puerto serie
    # Asegúrate que el hilo se inicia como daemon para que termine con la app principal
    serial_reader_thread = threading.Thread(target=read_from_serial, daemon=True)
    serial_reader_thread.start()

    # Iniciar el servidor Flask con SocketIO
    print(f"Servidor Flask con SocketIO iniciando en http://{HTTP_HOST}:{HTTP_PORT}")
    # socketio.run(app, host=HTTP_HOST, port=HTTP_PORT, debug=True, use_reloader=False) # debug=True puede dar problemas con hilos a veces
    socketio.run(app, host=HTTP_HOST, port=HTTP_PORT, debug=False)