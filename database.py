import sqlite3
import os
import sys


def ruta_base():

    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))


def conectar():

    base_path = os.path.join(os.environ["APPDATA"], "DatosFisicos")

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    db_path = os.path.join(base_path, "datos.db")

    return sqlite3.connect(db_path)

#def reiniciar_base_datos():

    if os.path.exists("dist/data/datos.db"):
        os.remove("dist/data/datos.db")

def crear_tablas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temporadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        temporada_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        equipo_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pruebas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id INTEGER,
        fecha TEXT,
        sprint30 REAL,
        illinois REAL,
        yoyo REAL
    )
    """)

    conn.commit()
    conn.close()

def obtener_temporadas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM temporadas")

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_equipos(temporada_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre FROM equipos WHERE temporada_id = ?",
        (temporada_id,)
    )

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_jugadores(equipo_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre FROM jugadores WHERE equipo_id = ?",
        (equipo_id,)
    )

    datos = cursor.fetchall()

    conn.close()

    return datos

def guardar_prueba(jugador_id, fecha, sprint30, illinois, yoyo):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pruebas
    (jugador_id, fecha, sprint30, illinois, yoyo)
    VALUES (?, ?, ?, ?, ?)
    """, (jugador_id, fecha, sprint30, illinois, yoyo))

    conn.commit()
    conn.close()

def obtener_resultados():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT jugadores.nombre,
           pruebas.sprint30,
           pruebas.illinois,
           pruebas.yoyo,
           pruebas.fecha
    FROM pruebas
    JOIN jugadores ON pruebas.jugador_id = jugadores.id
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_resultados_filtrados():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT equipos.nombre,
           jugadores.nombre,
           pruebas.fecha,
           pruebas.sprint30,
           pruebas.illinois,
           pruebas.yoyo
    FROM pruebas
    JOIN jugadores ON pruebas.jugador_id = jugadores.id
    JOIN equipos ON jugadores.equipo_id = equipos.id
    ORDER BY equipos.nombre, jugadores.nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_resultados_jugador(jugador_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT sprint30, illinois, yoyo
    FROM pruebas
    WHERE jugador_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (jugador_id,))

    datos = cursor.fetchone()

    conn.close()

    return datos

def obtener_todos_jugadores():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM jugadores")

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_historial_jugador(jugador_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fecha, sprint30, illinois, yoyo
    FROM pruebas
    WHERE jugador_id = ?
    ORDER BY fecha
    """, (jugador_id,))

    datos = cursor.fetchall()

    conn.close()

    return datos

def añadir_equipo(nombre, temporada_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO equipos (nombre, temporada_id)
    VALUES (?, ?)
    """, (nombre, temporada_id))

    conn.commit()
    conn.close()

def añadir_jugador(nombre, equipo_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jugadores (nombre, equipo_id)
    VALUES (?, ?)
    """, (nombre, equipo_id))

    conn.commit()
    conn.close()

def borrar_jugador(jugador_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jugadores WHERE id = ?", (jugador_id,))

    conn.commit()
    conn.close()

def borrar_equipo(equipo_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jugadores WHERE equipo_id = ?", (equipo_id,))
    cursor.execute("DELETE FROM equipos WHERE id = ?", (equipo_id,))

    conn.commit()
    conn.close()

def obtener_jugadores_equipo(equipo_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nombre
    FROM jugadores
    WHERE equipo_id = ?
    """, (equipo_id,))

    datos = cursor.fetchall()

    conn.close()

    return datos

def insertar_temporada(nombre):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO temporadas (nombre)
    VALUES (?)
    """, (nombre,))

    conn.commit()
    conn.close()