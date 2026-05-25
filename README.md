# Taller Docker en Codespaces

Guía de comandos para seguir la práctica. La explicación y narrativa completa están en la guía del instructor; este README está pensado para que los asistentes puedan copiar y ejecutar sin batallar.

## 0. Preparar Codespaces

Confirma que Docker está disponible:

```bash
docker --version
docker compose version
```

Ver contenedores activos:

```bash
docker ps
```

Ver todos los contenedores, incluso detenidos:

```bash
docker ps -a
```

## 1. Demo 1: telemetría industrial

Levanta el stack industrial:

```bash
cd demo1_iot
docker compose up -d --build
```

Abre el puerto `3000` en Codespaces.

Credenciales de Grafana:

```text
Usuario: admin
Password: admin
```

Ver logs del simulador:

```bash
docker compose logs -f simulador
```

Validar que InfluxDB tenga datos:

```bash
docker compose exec influxdb influx -database planta -execute 'SHOW MEASUREMENTS'
docker compose exec influxdb influx -database planta -execute 'SELECT * FROM maquina_industrial ORDER BY time DESC LIMIT 3'
```

Apagar Demo 1:

```bash
docker compose down
```

Apagar y borrar volúmenes/datos:

```bash
docker compose down -v
```

Volver a la raíz:

```bash
cd ..
```

## 2. Demo 1.5: contenedores efímeros y volúmenes

### Sin volumen

Crear un contenedor que escribe un archivo dentro de sí mismo:

```bash
docker run --name demo-efimero alpine sh -c "echo 'dato importante' > /dato.txt && cat /dato.txt"
```

Ver el contenedor detenido:

```bash
docker ps -a
```

Borrar el contenedor:

```bash
docker rm demo-efimero
```

Crear otro contenedor e intentar leer el archivo:

```bash
docker run --name demo-efimero-2 alpine sh -c "cat /dato.txt"
```

Limpiar:

```bash
docker rm demo-efimero-2
```

### Con volumen

Crear un volumen:

```bash
docker volume create demo-data
```

Escribir un archivo en el volumen:

```bash
docker run --name demo-volumen -v demo-data:/data alpine sh -c "echo 'dato importante' > /data/dato.txt && cat /data/dato.txt"
```

Borrar el contenedor:

```bash
docker rm demo-volumen
```

Crear otro contenedor usando el mismo volumen:

```bash
docker run --name demo-volumen-2 -v demo-data:/data alpine cat /data/dato.txt
```

Limpiar:

```bash
docker rm demo-volumen-2
docker volume rm demo-data
```

## 3. Demo 2: app de mantenimiento

Entrar a la demo:

```bash
cd demo2_app
```

Levantar frontend, backend y PostgreSQL:

```bash
docker compose up -d --build
```

Abrir la app web en el puerto `8081`.

Abrir la API en el puerto `8000` agregando `/docs` a la URL.

Ver contenedores de la demo:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Probar persistencia:

```bash
docker compose down
docker compose up -d --build
```

Borrar contenedores y datos:

```bash
docker compose down -v
```

## 4. Revisar PostgreSQL con TablePlus

Datos de conexión:

```text
Host: localhost
Port: 5433
User: postgres
Password: postgres
Database: workshop
Table: eventos_mantenimiento
```

Si usas Codespaces desde el navegador, crea un túnel local con GitHub CLI:

```bash
gh codespace list
gh codespace ports forward 5433:5433 -c NOMBRE_DEL_CODESPACE
```

Si el puerto local `5433` está ocupado:

```bash
gh codespace ports forward 5433:15433 -c NOMBRE_DEL_CODESPACE
```

En ese caso usa `localhost:15433` en TablePlus.

## 5. Demo 3: n8n con volumen

Si vienes de Demo 2:

```bash
cd ../demo3_n8n
```

Si estás en la raíz del repo:

```bash
cd demo3_n8n
```

Levantar n8n:

```bash
docker compose up -d
```

Abrir n8n en el puerto `5678`.

Probar persistencia:

```bash
docker compose down
docker compose up -d
```

Borrar n8n y su volumen:

```bash
docker compose down -v
```

Volver a la raíz:

```bash
cd ..
```

## Puertos usados

| Puerto | Servicio | Demo |
| --- | --- | --- |
| `3000` | Grafana | Demo 1 |
| `1883` | Mosquitto MQTT | Demo 1 |
| `8086` | InfluxDB | Demo 1 |
| `8081` | Nginx frontend | Demo 2 |
| `8000` | FastAPI backend | Demo 2 |
| `5433` | PostgreSQL | Demo 2 |
| `5678` | n8n | Demo 3 |

## Comandos rápidos

Levantar una demo con Compose:

```bash
docker compose up -d --build
```

Ver servicios de una demo:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Apagar sin borrar volúmenes:

```bash
docker compose down
```

Apagar y borrar volúmenes:

```bash
docker compose down -v
```
