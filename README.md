
**Paso 1: Levantar todos los servicios**
Abre una terminal en la parte inferior de Codespaces (`Ctrl + Ñ` o `Cmd + J`) y ejecuta:
```bash
cd demo1_iot
docker-compose up -d
```
*(Ve a la pestaña "Ports" de Codespaces y abre la URL del puerto **3000**).*

**Paso 2: Iniciar el simulador del sensor**
Abre una **nueva pestaña** de terminal (botón `+` en la terminal) y ejecuta:
```bash
cd demo1_iot
pip install -r requirements.txt
python simulador_sensor.py
```

**Paso 3: Detener la Demo 1**
En la primera terminal, asegúrate de estar en `demo1_iot` y apaga los servicios para liberar memoria:
```bash
docker-compose down
```

**Paso 4: Crear la imagen de la API (Dockerfile)**
En el explorador de archivos a tu izquierda, abre `demo2_app/backend/Dockerfile` y pega esta receta:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Paso 5: Orquestación (Docker Compose)**
En el explorador, abre el archivo `demo2_app/docker-compose.yml` y pega la infraestructura completa:

```yaml
version: '3.8'

services:
  frontend:
    image: nginx:alpine
    ports: ["8080:80"]
    volumes:
      - ./frontend/index.html:/usr/share/nginx/html/index.html
      - ./frontend/default.conf:/etc/nginx/conf.d/default.conf
    networks:
      - app_network
  
  backend:
    build: ./backend
    environment:
      - DB_HOST=db
      - DB_NAME=workshop
      - DB_USER=postgres
      - DB_PASS=postgres
    networks:
      - app_network
  
  db:
    image: postgres:15-alpine
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
docker-compose up -d --build
```
*(Ve a la pestaña "Ports", abre el puerto **8080** y prueba la página web).*
