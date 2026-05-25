# Demo 3: n8n con volumen

Mini demo para mostrar un caso realista de persistencia con Docker Compose.

La idea base de contenedores efímeros ya se demuestra en `demo1_5_volumes_basico`. Aquí usamos n8n para ver cómo una app real conserva su configuración y workflows usando un volumen nombrado.

## Levantar n8n

```bash
cd demo3_n8n
docker compose up -d
```

Abre el puerto `5678`, crea una cuenta local de prueba y arma un workflow sencillo.

## Probar persistencia

Destruye y recrea los contenedores:

```bash
docker compose down
docker compose up -d
```

Al volver a entrar, la configuración y los workflows siguen ahí porque viven en el volumen `n8n-data`.

## Borrar la persistencia

```bash
docker compose down -v
```

## Idea para explicar

El contenedor de n8n puede borrarse y crearse otra vez. El volumen `n8n-data` queda fuera de ese ciclo y por eso conserva los datos.
