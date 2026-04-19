import sqlite3, logging

from core.RUTAS import *

logger = logging.getLogger("LOGS")


def Leer_crear_db():
    
    try:
        with sqlite3.connect(ruta_db_registro) as conn:
            cursor = conn.cursor()
            
            cursor.execute ("""
                            CREATE TABLE IF NOT EXISTS metadatos_db (
                                id TEXT PRIMARY KEY UNIQUE,
                                tipo TEXT,
                                nombre TEXT,
                                origen TEXT,
                                fecha TEXT
                            )
                            """)
        
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {e}")
        
    
    try:
        with sqlite3.connect(ruta_db_registro) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tipo, nombre, origen, fecha FROM metadatos_db ORDER BY fecha DESC")
            datos = cursor.fetchall()

        return datos

    except Exception as e:
        logger.error(f"Error al leer la base de datos: {e}")
        return False

