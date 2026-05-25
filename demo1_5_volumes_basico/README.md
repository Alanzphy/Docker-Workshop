# Demo 1.5: contenedores efímeros y volúmenes

Mini demo sin Docker Compose para explicar la idea base:

- Un contenedor es reemplazable.
- Los datos escritos dentro del contenedor se pierden cuando el contenedor se elimina.
- Un volumen guarda datos fuera del ciclo de vida del contenedor.

## Parte 1: sin volumen

Crea un contenedor que escribe un archivo dentro de su filesystem:

```bash
docker run --name demo-efimero alpine sh -c "echo 'dato importante' > /dato.txt && cat /dato.txt"
```

El contenedor termina, pero todavía existe detenido:

```bash
docker ps -a
```

Mientras el contenedor existe, puedes leer el archivo:

```bash
docker start -ai demo-efimero
```

Borra el contenedor:

```bash
docker rm demo-efimero
```

Crea otro contenedor e intenta leer el archivo:

```bash
docker run --name demo-efimero-2 alpine sh -c "cat /dato.txt"
```

Debe fallar porque `/dato.txt` vivía dentro del contenedor anterior.

Limpia el contenedor de prueba:

```bash
docker rm demo-efimero-2
```

## Parte 2: con volumen

Crea un volumen:

```bash
docker volume create demo-data
```

Crea un contenedor que escribe en el volumen:

```bash
docker run --name demo-volumen -v demo-data:/data alpine sh -c "echo 'dato importante' > /data/dato.txt && cat /data/dato.txt"
```

Borra el contenedor:

```bash
docker rm demo-volumen
```

Crea otro contenedor usando el mismo volumen:

```bash
docker run --name demo-volumen-2 -v demo-data:/data alpine cat /data/dato.txt
```

El dato sigue apareciendo porque vive en `demo-data`, no en el contenedor.

Limpia la demo:

```bash
docker rm demo-volumen-2
docker volume rm demo-data
```

## Idea para explicar

Sin volumen, el dato muere con el contenedor.

Con volumen, el contenedor puede morir y el dato sigue vivo.

Docker Compose aplica la misma idea, solo que administra varios contenedores y volúmenes juntos.
