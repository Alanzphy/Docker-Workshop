from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "workshop"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "postgres")
    )
    return conn

# Inicialización de la base de datos (se ejecuta al arrancar el contenedor de python)
try:
    conn = get_db_connection()
    cur = conn.cursor()
    # Creamos la tabla si no existe
    cur.execute("CREATE TABLE IF NOT EXISTS visitas (id SERIAL PRIMARY KEY, cantidad INT);")
    # Insertamos la fila inicial en 0 si la tabla está vacía
    cur.execute("INSERT INTO visitas (cantidad) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM visitas);")
    conn.commit()
    cur.close()
    conn.close()
    print("Base de datos inicializada correctamente.")
except Exception as e:
    print(f"Error inicializando BD (puede que el contenedor de BD aún esté arrancando): {e}")

@app.get("/api/visitas")
def get_visitas():
    conn = get_db_connection()
    cur = conn.cursor()
    # Incrementar el contador de forma atómica y devolver el nuevo valor
    cur.execute("UPDATE visitas SET cantidad = cantidad + 1 RETURNING cantidad;")
    visitas = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"visitas": visitas}
