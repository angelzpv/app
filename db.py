import sqlite3

def crear_tablas():
    conn = sqlite3.connect("zona90.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(usuario, email, password):
    conn = sqlite3.connect("zona90.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, email, password) VALUES (?, ?, ?)", (usuario, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validar_usuario(usuario, email, password):
    conn = sqlite3.connect("zona90.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND email=? AND password=?", (usuario, email, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
