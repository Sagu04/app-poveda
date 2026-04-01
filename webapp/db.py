import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "datos.db")

def conectar():
    return sqlite3.connect(DB_PATH)


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
        nombre TEXT NOT NULL,
        codigo_equipo INTEGER,
        temporada_id INTEGER NOT NULL,
        FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        equipo_id INTEGER,
        FOREIGN KEY (equipo_id) REFERENCES equipos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pruebas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id INTEGER,
        fecha TEXT,
        sprint30 REAL,
        illinois REAL,
        yoyo REAL,
        FOREIGN KEY (jugador_id) REFERENCES jugadores(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_prueba (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        unidad TEXT,
        temporada_id INTEGER NOT NULL,
        FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados_prueba (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jugador_id INTEGER NOT NULL,
        prueba_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY (jugador_id) REFERENCES jugadores(id),
        FOREIGN KEY (prueba_id) REFERENCES tipos_prueba(id)
    )
    """)

    try:
        cursor.execute("ALTER TABLE equipos ADD COLUMN codigo_equipo INTEGER")
    except:
        pass

    conn.commit()
    conn.close()


def obtener_temporadas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM temporadas ORDER BY nombre")
    datos = cursor.fetchall()
    conn.close()
    return datos


def insertar_temporada(nombre):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO temporadas (nombre) VALUES (?)", (nombre,))
    temporada_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return temporada_id

def obtener_temporada_por_id(temporada_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM temporadas WHERE id = ?", (temporada_id,))
    dato = cursor.fetchone()
    conn.close()
    return dato


def obtener_equipos_por_temporada(temporada_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM equipos
        WHERE temporada_id = ?
    """, (temporada_id,))

    datos = cursor.fetchall()
    conn.close()

    categorias = [
        "Senior",
        "Juvenil",
        "Cadete",
        "Infantil",
        "Alevín",
        "Benjamín",
        "Prebenjamín"
    ]

    equipos_por_categoria = {cat: [] for cat in categorias}
    equipos_por_categoria["Otros"] = []

    # Clasificar equipos
    for equipo in datos:
        nombre = equipo[1]
        encontrado = False

        for cat in categorias:
            if nombre.startswith(cat):
                equipos_por_categoria[cat].append(equipo)
                encontrado = True
                break

        if not encontrado:
            equipos_por_categoria["Otros"].append(equipo)

    # Ordenar dentro de cada categoría (A, B, C...)
    for cat in equipos_por_categoria:
        equipos_por_categoria[cat] = sorted(equipos_por_categoria[cat], key=lambda x: x[1])

    return equipos_por_categoria

    def clave_orden(equipo):
        nombre = equipo[1]

        for i, categoria in enumerate(orden_categorias):
            if nombre.startswith(categoria):
                return i

        return len(orden_categorias)

    return sorted(datos, key=clave_orden)


def insertar_equipo(nombre, temporada_id, codigo_equipo=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO equipos (nombre, temporada_id, codigo_equipo)
        VALUES (?, ?, ?)
    """, (nombre, temporada_id, codigo_equipo))

    conn.commit()
    conn.close()


def obtener_equipo_por_id(equipo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, temporada_id FROM equipos WHERE id = ?", (equipo_id,))
    dato = cursor.fetchone()
    conn.close()
    return dato


def obtener_jugadores_por_equipo(equipo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre
        FROM jugadores
        WHERE equipo_id = ?
        ORDER BY nombre
    """, (equipo_id,))
    datos = cursor.fetchall()
    conn.close()
    return datos


def insertar_jugador(nombre, equipo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jugadores (nombre, equipo_id)
        VALUES (?, ?)
    """, (nombre, equipo_id))
    conn.commit()
    conn.close()


def obtener_jugador_por_id(jugador_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, equipo_id
        FROM jugadores
        WHERE id = ?
    """, (jugador_id,))
    dato = cursor.fetchone()

    conn.close()
    return dato


def insertar_prueba(jugador_id, fecha, sprint30, illinois, yoyo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pruebas (jugador_id, fecha, sprint30, illinois, yoyo)
        VALUES (?, ?, ?, ?, ?)
    """, (jugador_id, fecha, sprint30, illinois, yoyo))

    conn.commit()
    conn.close()


def obtener_pruebas_por_jugador(jugador_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fecha, sprint30, illinois, yoyo
        FROM pruebas
        WHERE jugador_id = ?
        ORDER BY fecha DESC
    """, (jugador_id,))
    datos = cursor.fetchall()

    conn.close()
    return datos

def obtener_resultados(equipo_id=None, categoria=None, grupo=None):
    conn = conectar()
    cursor = conn.cursor()

    query = """
    SELECT jugadores.nombre, pruebas.fecha,
           pruebas.sprint30, pruebas.illinois, pruebas.yoyo,
           equipos.nombre
    FROM pruebas
    JOIN jugadores ON pruebas.jugador_id = jugadores.id
    JOIN equipos ON jugadores.equipo_id = equipos.id
    """

    condiciones = []
    params = []

    if equipo_id:
        condiciones.append("equipos.id = ?")
        params.append(equipo_id)

    if categoria:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"{categoria}%")

    if grupo:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"% {grupo}")

    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    query += " ORDER BY equipos.nombre, jugadores.nombre, pruebas.fecha DESC"

    cursor.execute(query, params)
    datos = cursor.fetchall()

    conn.close()
    return datos

def obtener_todos_equipos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM equipos ORDER BY nombre")
    datos = cursor.fetchall()

    conn.close()
    return datos

def obtener_datos_grafica(jugador_id):
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

def obtener_todos_jugadores():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM jugadores ORDER BY nombre")
    datos = cursor.fetchall()

    conn.close()
    return datos

def eliminar_jugador(jugador_id):
    conn = conectar()
    cursor = conn.cursor()

    # borrar primero las pruebas del jugador
    cursor.execute("DELETE FROM pruebas WHERE jugador_id = ?", (jugador_id,))

    # luego borrar el jugador
    cursor.execute("DELETE FROM jugadores WHERE id = ?", (jugador_id,))

    conn.commit()
    conn.close()

def eliminar_equipo(equipo_id):
    conn = conectar()
    cursor = conn.cursor()

    # borrar pruebas de los jugadores del equipo
    cursor.execute("""
        DELETE FROM pruebas
        WHERE jugador_id IN (
            SELECT id FROM jugadores WHERE equipo_id = ?
        )
    """, (equipo_id,))

    # borrar jugadores
    cursor.execute("DELETE FROM jugadores WHERE equipo_id = ?", (equipo_id,))

    # borrar equipo
    cursor.execute("DELETE FROM equipos WHERE id = ?", (equipo_id,))

    conn.commit()
    conn.close()


def eliminar_temporada(temporada_id):
    conn = conectar()
    cursor = conn.cursor()

    # borrar pruebas
    cursor.execute("""
        DELETE FROM pruebas
        WHERE jugador_id IN (
            SELECT jugadores.id
            FROM jugadores
            JOIN equipos ON jugadores.equipo_id = equipos.id
            WHERE equipos.temporada_id = ?
        )
    """, (temporada_id,))

    # borrar jugadores
    cursor.execute("""
        DELETE FROM jugadores
        WHERE equipo_id IN (
            SELECT id FROM equipos WHERE temporada_id = ?
        )
    """, (temporada_id,))

    # borrar equipos
    cursor.execute("DELETE FROM equipos WHERE temporada_id = ?", (temporada_id,))

    # borrar temporada
    cursor.execute("DELETE FROM temporadas WHERE id = ?", (temporada_id,))

    conn.commit()
    conn.close()


def actualizar_jugador(jugador_id, nuevo_nombre):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jugadores
        SET nombre = ?
        WHERE id = ?
    """, (nuevo_nombre, jugador_id))

    conn.commit()
    conn.close()

def obtener_categorias():
    return [
        "Senior",
        "Juvenil",
        "Cadete",
        "Infantil",
        "Alevín",
        "Benjamín",
        "Prebenjamín"
    ]

def obtener_jugadores_filtrados(categoria=None, grupo=None):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT jugadores.id, jugadores.nombre
        FROM jugadores
        JOIN equipos ON jugadores.equipo_id = equipos.id
    """

    condiciones = []
    params = []

    if categoria:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"{categoria}%")

    if grupo:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"% {grupo}")

    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    query += " ORDER BY jugadores.nombre"

    cursor.execute(query, params)
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_grupos():
    return [
        "Masc",
        "Fem",
        "A",
        "B",
        "C",
        "D"
    ]

def insertar_tipo_prueba(nombre, unidad, temporada_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tipos_prueba (nombre, unidad, temporada_id)
        VALUES (?, ?, ?)
    """, (nombre, unidad, temporada_id))

    conn.commit()
    conn.close()


def obtener_pruebas_por_temporada(temporada_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, unidad
        FROM tipos_prueba
        WHERE temporada_id = ?
        ORDER BY nombre
    """, (temporada_id,))

    datos = cursor.fetchall()
    conn.close()
    return datos


def eliminar_tipo_prueba(prueba_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tipos_prueba WHERE id = ?", (prueba_id,))

    conn.commit()
    conn.close()

def obtener_temporada_de_jugador(jugador_id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT temporadas.id, temporadas.nombre
            FROM jugadores
            JOIN equipos ON jugadores.equipo_id = equipos.id
            JOIN temporadas ON equipos.temporada_id = temporadas.id
            WHERE jugadores.id = ?
        """, (jugador_id,))

        dato = cursor.fetchone()
        conn.close()
        return dato

def insertar_resultado_prueba(jugador_id, prueba_id, fecha, valor):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO resultados_prueba (jugador_id, prueba_id, fecha, valor)
            VALUES (?, ?, ?, ?)
        """, (jugador_id, prueba_id, fecha, valor))

        conn.commit()
        conn.close()

def obtener_resultados_dinamicos_jugador(jugador_id):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT tipos_prueba.nombre, tipos_prueba.unidad, resultados_prueba.fecha, resultados_prueba.valor
            FROM resultados_prueba
            JOIN tipos_prueba ON resultados_prueba.prueba_id = tipos_prueba.id
            WHERE resultados_prueba.jugador_id = ?
            ORDER BY resultados_prueba.fecha DESC, tipos_prueba.nombre
        """, (jugador_id,))

        datos = cursor.fetchall()
        conn.close()
        return datos

def obtener_resultados_dinamicos(equipo_id=None, categoria=None, grupo=None):
    conn = conectar()
    cursor = conn.cursor()

    query = """
    SELECT equipos.nombre, jugadores.nombre, resultados_prueba.fecha,
           tipos_prueba.nombre, resultados_prueba.valor, tipos_prueba.unidad
    FROM resultados_prueba
    JOIN jugadores ON resultados_prueba.jugador_id = jugadores.id
    JOIN equipos ON jugadores.equipo_id = equipos.id
    JOIN tipos_prueba ON resultados_prueba.prueba_id = tipos_prueba.id
    """

    condiciones = []
    params = []

    if equipo_id:
        condiciones.append("equipos.id = ?")
        params.append(equipo_id)

    if categoria:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"{categoria}%")

    if grupo:
        condiciones.append("equipos.nombre LIKE ?")
        params.append(f"% {grupo}")

    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    query += " ORDER BY equipos.nombre, jugadores.nombre, resultados_prueba.fecha DESC"

    cursor.execute(query, params)
    datos = cursor.fetchall()

    conn.close()
    return datos


def obtener_datos_grafica_dinamicos(jugador_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tipos_prueba.nombre, tipos_prueba.unidad, resultados_prueba.fecha, resultados_prueba.valor
        FROM resultados_prueba
        JOIN tipos_prueba ON resultados_prueba.prueba_id = tipos_prueba.id
        WHERE resultados_prueba.jugador_id = ?
        ORDER BY tipos_prueba.nombre, resultados_prueba.fecha
    """, (jugador_id,))

    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_equipo_por_codigo(codigo_equipo, temporada_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM equipos
        WHERE codigo_equipo = ? AND temporada_id = ?
    """, (codigo_equipo, temporada_id))

    dato = cursor.fetchone()
    conn.close()
    return dato

def insertar_jugador_si_no_existe(nombre, equipo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM jugadores
        WHERE nombre = ? AND equipo_id = ?
    """, (nombre, equipo_id))

    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO jugadores (nombre, equipo_id)
            VALUES (?, ?)
        """, (nombre, equipo_id))

    conn.commit()
    conn.close()

def insertar_equipo_si_no_existe(nombre, temporada_id, codigo_equipo=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM equipos
        WHERE nombre = ? AND temporada_id = ?
    """, (nombre, temporada_id))

    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO equipos (nombre, temporada_id, codigo_equipo)
            VALUES (?, ?, ?)
        """, (nombre, temporada_id, codigo_equipo))

    conn.commit()
    conn.close()

def temporada_existe(nombre):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM temporadas WHERE nombre = ?", (nombre,))
    existe = cursor.fetchone()

    conn.close()
    return existe is not None