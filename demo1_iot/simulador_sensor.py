import paho.mqtt.client as mqtt
import time
import random

# Configuración del broker MQTT
BROKER = "localhost" # En Codespaces, los puertos mapeados al host funcionan como localhost
PORT = 1883
TOPIC = "sensores/temperatura"

client = mqtt.Client()

print(f"Conectando al broker MQTT en {BROKER}:{PORT}...")
try:
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"Error de conexión: {e}. Asegúrate de que los contenedores están corriendo.")
    exit(1)

print("¡Conectado! Iniciando simulación de sensor. Presiona Ctrl+C para detener.")
try:
    temperatura_base = 25.0
    while True:
        # Generar un dato con ligera variación
        temperatura = temperatura_base + random.uniform(-2.0, 2.0)
        
        # Publicar el dato
        client.publish(TOPIC, str(temperatura))
        print(f"Enviado: {temperatura:.2f} °C al topic '{TOPIC}'")
        
        time.sleep(2) # Enviar dato cada 2 segundos
except KeyboardInterrupt:
    print("\nSimulación detenida.")
finally:
    client.disconnect()
