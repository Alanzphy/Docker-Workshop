import os
import random
import time
from contextlib import closing

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException

app = FastAPI()

EVENTOS_DEMO = [
    ("Inspeccion", "Revision visual de banda transportadora y guardas de seguridad."),
    ("Lubricacion", "Lubricacion preventiva de chumaceras del motor principal."),
    ("Ajuste", "Ajuste de tension en banda por variacion de vibracion."),
    ("Alerta", "Seguimiento a lectura alta de temperatura en motor."),
    ("Cambio", "Cambio preventivo de filtro en sistema hidraulico."),
]


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "workshop"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "postgres"),
    )


def ensure_database(max_retries=20):
    last_error = None

    for intento in range(1, max_retries + 1):
        try:
            with closing(get_db_connection()) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS eventos_mantenimiento (
                            id SERIAL PRIMARY KEY,
                            maquina TEXT NOT NULL,
                            tipo TEXT NOT NULL,
                            descripcion TEXT NOT NULL,
                            creado_en TIMESTAMP NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                conn.commit()
            return
        except Exception as error:
            last_error = error
            print(f"Base de datos no disponible todavia ({intento}/{max_retries}): {error}")
            time.sleep(1)

    raise HTTPException(status_code=503, detail=f"Base de datos no disponible: {last_error}")


def obtener_resumen():
    ensure_database()

    with closing(get_db_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) AS total FROM eventos_mantenimiento;")
            total = cur.fetchone()["total"]

            cur.execute(
                """
                SELECT id, maquina, tipo, descripcion, creado_en
                FROM eventos_mantenimiento
                ORDER BY creado_en DESC, id DESC
                LIMIT 5;
                """
            )
            eventos = [dict(evento) for evento in cur.fetchall()]

    return {"total": total, "eventos": eventos}


@app.get("/api/eventos")
def listar_eventos():
    return obtener_resumen()


@app.post("/api/eventos")
def registrar_evento():
    ensure_database()
    tipo, descripcion = random.choice(EVENTOS_DEMO)

    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO eventos_mantenimiento (maquina, tipo, descripcion)
                VALUES (%s, %s, %s);
                """,
                ("Motor-Banda-01", tipo, descripcion),
            )
        conn.commit()

    return obtener_resumen()
