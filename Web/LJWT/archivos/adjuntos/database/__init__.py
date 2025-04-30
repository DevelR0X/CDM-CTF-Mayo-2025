from secret import CODEX_PROJECT_SECRETS

import sqlite3
import os

DATABASE = 'database.db'

def init_db():
    """Inicializar base de datos"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY, 
                  name TEXT, 
                  record TEXT, 
                  access_level INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, 
                  username TEXT, 
                  password TEXT, 
                  email TEXT, 
                  access_level INTEGER DEFAULT 1)''')

    admin_password = os.urandom(32).hex()
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
              (1, 'Administrador', admin_password, 'admin@hed.cl', 3))

    c.execute("INSERT OR IGNORE INTO doctors VALUES (?, ?, ?, ?)",
              (1, 'John Doe', 'Sin novedades', 1))

    c.execute("INSERT OR IGNORE INTO doctors VALUES (?, ?, ?, ?)",
              (2, 'Dr. Brinck', CODEX_PROJECT_SECRETS, 3))

    conn.commit()
    conn.close()
