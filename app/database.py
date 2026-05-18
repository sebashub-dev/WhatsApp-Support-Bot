import sqlite3

def init_db():
    with sqlite3.connect("conversations.db") as con:
        cursor = con.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        role TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP) """
    )

def save_message(numero, role, mensaje):
    with sqlite3.connect("conversations.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO mensajes (numero, role, mensaje) VALUES (?, ?, ?)",
            (numero, role, mensaje)
        )

def get_history(number):
    with sqlite3.connect("conversations.db") as con:
        cursor = con.cursor()
        cursor.execute(
            """SELECT role, mensaje FROM mensajes 
                WHERE numero = ?
                AND timestamp > datetime('now', '-3 days')
                ORDER BY timestamp ASC
                LIMIT 10 """,(number,)
        )
        return cursor.fetchall()