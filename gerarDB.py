import pyodbc
import sqlite3
import os

if os.path.exists('usuarios.db'):
    os.remove('usuarios.db')

conn_sql = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=VICTOR;'
    'DATABASE=API;'
    'UID=admin;'
    'PWD=admin;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)
cursor_sql = conn_sql.cursor()

conn_sqlite = sqlite3.connect('usuarios.db')
cursor_sqlite = conn_sqlite.cursor()

cursor_sqlite.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
''')
conn_sqlite.commit()  

cursor_sql.execute("SELECT usuario, senha FROM Usuarios")
usuarios = cursor_sql.fetchall()

for usuario, senha in usuarios:
    cursor_sqlite.execute("INSERT INTO Usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))

conn_sqlite.commit()
conn_sqlite.close()
conn_sql.close()

print("Banco SQLite criado com sucesso!")
