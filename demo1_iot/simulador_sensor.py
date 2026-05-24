import json
import os
import random
import time

import paho.mqtt.client as mqtt

# Configuración del broker MQTT
BROKER = os.environ.get("MQTT_BROKER", "localhost")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
TOPIC = "planta/linea1/maquina1/telemetria"
MAQUINA = os.environ.get("MAQUINA_ID", "Motor-Banda-01")
LINEA = os.environ.get("LINEA_ID", "Linea-1")


def calcular_estado(ciclo):
    fase = ciclo % 36

    if fase < 18:
        return "normal", 0, 0.0
    if fase < 28:
        return "advertencia", 1, (fase - 18) / 10
    return "falla", 2, 1.0


def generar_telemetria(ciclo):
    estado, estado_codigo, carga_falla = calcular_estado(ciclo)

    temperatura = 58 + (24 * carga_falla) + random.uniform(-1.8, 2.4)
    vibracion = 2.2 + (6.5 * carga_falla) + random.uniform(-0.3, 0.5)
    rpm = 1760 - (260 * carga_falla) + random.uniform(-35, 35)
    presion = 6.2 + (2.1 * carga_falla) + random.uniform(-0.2, 0.25)
    piezas_por_minuto = 42 - (18 * carga_falla) + random.uniform(-2, 2)

    if estado == "falla":
        rpm = max(900, rpm - random.uniform(80, 180))
        piezas_por_minuto = max(8, piezas_por_minuto - random.uniform(4, 8))

    return {
        "maquina": MAQUINA,
        "linea": LINEA,
        "estado": estado,
        "estado_codigo": estado_codigo,
        "temperatura_motor": round(temperatura, 2),
        "vibracion_mm_s": round(vibracion, 2),
        "rpm": round(rpm, 0),
        "presion_bar": round(presion, 2),
        "piezas_por_minuto": round(piezas_por_minuto, 1),
    }


client = mqtt.Client()

print(f"Conectando al broker MQTT en {BROKER}:{PORT}...")
for intento in range(1, 31):
    try:
        client.connect(BROKER, PORT, 60)
        break
    except Exception as e:
        print(f"Broker no disponible todavía ({intento}/30): {e}")
        time.sleep(2)
else:
    print("No se pudo conectar al broker MQTT. Asegúrate de que los contenedores están corriendo.")
    exit(1)

client.loop_start()

print(f"Conectado. Simulando la máquina industrial '{MAQUINA}'. Presiona Ctrl+C para detener.")
try:
    ciclo = 0
    while True:
        telemetria = generar_telemetria(ciclo)
        payload = json.dumps(telemetria)

        client.publish(TOPIC, payload)
        print(
            "Enviado: "
            f"{telemetria['estado'].upper()} | "
            f"Temp {telemetria['temperatura_motor']:.2f} °C | "
            f"Vib {telemetria['vibracion_mm_s']:.2f} mm/s | "
            f"RPM {telemetria['rpm']:.0f} | "
            f"{telemetria['piezas_por_minuto']:.1f} pzs/min"
        )

        ciclo += 1
        time.sleep(2)
except KeyboardInterrupt:
    print("\nSimulación detenida.")
finally:
    client.loop_stop()
    client.disconnect()
