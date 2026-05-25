# Taller Docker en Codespaces

Repositorio para un taller práctico de Docker usando GitHub Codespaces. La idea es que los asistentes no instalen nada localmente: abren el Codespace, levantan servicios con `docker compose` y ven cómo Docker permite correr arquitecturas completas de forma repetible.

## Qué se construye

**Demo 1: máquina industrial + monitoreo**

Un simulador en Python genera señales industriales como temperatura, vibración, RPM, presión y producción. Los datos viajan por MQTT, Telegraf los guarda en InfluxDB y Grafana muestra el dashboard en vivo.

**Demo 2: app de mantenimiento + persistencia**

Una app web registra eventos de mantenimiento. El frontend corre en Nginx, la API en FastAPI y los datos se guardan en PostgreSQL usando un volumen de Docker.

## Abrir el repo en Codespaces

1. En GitHub, entra al repositorio.
2. Presiona `Code`.
3. Abre la pestaña `Codespaces`.
4. Crea un Codespace nuevo.
5. Espera a que VS Code termine de preparar el ambiente.

Para confirmar que Docker está disponible:

```bash
docker --version
docker compose version
```

Si Codespaces abre un `Recovery Container` o muestra un error de firma GPG durante la creación del contenedor, reconstruye el Codespace después de traer la versión más reciente del repo. Este proyecto usa una imagen base `bookworm` para evitar problemas con repositorios antiguos de Debian/Yarn.

## Demo 1: telemetría industrial

Levanta la arquitectura completa:

```bash
cd demo1_iot
docker compose up -d --build
```

En la pestaña `Ports` de Codespaces abre el puerto `3000`.

Credenciales de Grafana:

```text
Usuario: admin
Password: admin
```

El dashboard ya aparece provisionado con datos en vivo. Si al inicio se ve plano, espera un minuto y deja el rango de Grafana en los últimos 3 minutos para ver mejor las variaciones.

Para ver las lecturas desde terminal:

```bash
docker compose logs -f simulador
```

Cuando termines la Demo 1, apágala para liberar memoria:

```bash
docker compose down
```

## Demo 2: app con Dockerfile, red y volumen

Si vienes de la Demo 1:

```bash
cd ../demo2_app
docker compose up -d --build
```

Si estás en la raíz del repo, usa `cd demo2_app` antes de levantar los servicios.

Abre el puerto `8081` en la pestaña `Ports` para usar la app web.

También puedes abrir la API directamente en el puerto `8000` y agregar `/docs` al final de la URL:

```text
/docs
```

Ese endpoint muestra Swagger UI de FastAPI y sirve para enseñar que el backend es otro servicio dentro de la arquitectura.

## Probar persistencia con volumen

1. En la app web, registra algunos eventos.
2. Apaga los contenedores:

```bash
docker compose down
```

3. Levántalos de nuevo:

```bash
docker compose up -d --build
```

4. Abre otra vez el puerto `8081`.

Los eventos siguen ahí porque PostgreSQL guarda sus datos en el volumen `db-data`.

Para borrar la base y empezar desde cero:

```bash
docker compose down -v
```

## Conectar PostgreSQL con TablePlus

Con la Demo 2 levantada, la base usa estos datos:

```text
Host: localhost
Port: 5433
User: postgres
Password: postgres
Database: workshop
Table: eventos_mantenimiento
```

Si usas VS Code de escritorio conectado al Codespace, normalmente el puerto `5433` aparece como `localhost:5433` en tu Mac.

Si usas Codespaces desde el navegador, TablePlus necesita un túnel TCP local. En tu Mac, con GitHub CLI:

```bash
gh codespace list
gh codespace ports forward 5433:5433 -c NOMBRE_DEL_CODESPACE
```

También puedes filtrar por repo:

```bash
gh codespace ports forward 5433:5433 -R USUARIO/REPO
```

Si el puerto local `5433` está ocupado:

```bash
gh codespace ports forward 5433:15433 -c NOMBRE_DEL_CODESPACE
```

En ese caso, TablePlus usa `localhost` y puerto `15433`.

## Puertos usados

| Puerto | Servicio | Uso |
| --- | --- | --- |
| `3000` | Grafana | Dashboard de Demo 1 |
| `1883` | Mosquitto MQTT | Mensajes del simulador |
| `8086` | InfluxDB | Base de series de tiempo |
| `8081` | Nginx frontend | App web de Demo 2 |
| `8000` | FastAPI backend | API y Swagger UI |
| `5433` | PostgreSQL | Base de datos de mantenimiento |

## Comandos útiles

Ver contenedores activos:

```bash
docker ps
```

Ver logs de una demo:

```bash
docker compose logs -f
```

Apagar una demo sin borrar datos:

```bash
docker compose down
```

Apagar y borrar volúmenes:

```bash
docker compose down -v
```
