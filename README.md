
**Paso 1: Levantar todos los servicios**
Abre una terminal en la parte inferior de Codespaces (`Ctrl + Ñ` o `Cmd + J`) y ejecuta:
```bash
cd demo1_iot
docker compose up -d --build
```
*(Ve a la pestaña "Ports" de Codespaces y abre la URL del puerto **3000**. Entra con `admin` / `admin`; el dashboard de la máquina industrial ya aparece con datos en vivo).*

**Paso 2: Ver el simulador de la máquina industrial**
El simulador ya corre dentro de Docker. Si quieres ver sus lecturas en terminal:
```bash
cd demo1_iot
docker compose logs -f simulador
```
Vas a ver temperatura del motor, vibración, RPM, presión, piezas por minuto y el estado de la máquina cambiando entre `NORMAL`, `ADVERTENCIA` y `FALLA`.
Los estados de advertencia y falla aparecen automáticamente después de alrededor de un minuto.
Para ver mejor las curvas al inicio, deja el rango de Grafana en los últimos 3 minutos.

**Paso 3: Detener la Demo 1**
En la primera terminal, asegúrate de estar en `demo1_iot` y apaga los servicios para liberar memoria:
```bash
docker compose down
```

**Paso 4: Crear la imagen de la API (Dockerfile)**
En el explorador de archivos a tu izquierda, abre `demo2_app/backend/Dockerfile` y revisa esta receta:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Paso 5: Orquestación (Docker Compose)**
En el explorador, abre el archivo `demo2_app/docker-compose.yml` y revisa la infraestructura completa:

```yaml
services:
  frontend:
    image: nginx:alpine
    ports: ["8081:80"]
    volumes:
      - ./frontend/index.html:/usr/share/nginx/html/index.html
      - ./frontend/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
    networks:
      - app_network
  
  backend:
    build: ./backend
    environment:
      - DB_HOST=db
      - DB_NAME=workshop
      - DB_USER=postgres
      - DB_PASS=postgres
    depends_on:
      - db
    networks:
      - app_network
  
  db:
    image: postgres:15-alpine
    ports:
      - "5433:5432"
    environment:
      - POSTGRES_DB=workshop
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app_network

networks:
  app_network:
    driver: bridge
    
volumes:
  db-data:
```

**Paso 6: ¡Correr el proyecto!**
En la terminal, navega a la carpeta de la demo 2 y levanta el sistema:
```bash
cd ../demo2_app
docker compose up -d --build
```
*(Ve a la pestaña "Ports", abre el puerto **8081** y registra algunos eventos de mantenimiento).*

**Paso 7: Probar el volumen**
Apaga y vuelve a levantar la Demo 2:
```bash
docker compose down
docker compose up -d --build
```
Abre de nuevo el puerto **8081**. Los eventos siguen guardados porque PostgreSQL usa el volumen `db-data`.

**Opcional: Ver PostgreSQL en TablePlus**
Con la Demo 2 levantada, crea una conexión PostgreSQL con estos datos:
```text
Host: localhost
Port: 5433
User: postgres
Password: postgres
Database: workshop
```
La tabla de la demo se llama `eventos_mantenimiento`.

Si estás en **Codespaces desde el navegador**, TablePlus no se conecta a la URL `https://...app.github.dev`; necesita un puerto local TCP. Desde tu terminal local puedes crear el túnel con GitHub CLI:
```bash
gh codespace ports forward 5433:5433
```
Si tu puerto local `5433` está ocupado, usa otro puerto local:
```bash
gh codespace ports forward 5433:15433
```
En ese caso, en TablePlus usa `localhost` y puerto `15433`.
