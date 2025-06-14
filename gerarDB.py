import pyodbc
import sqlite3
import os
from decimal import Decimal

# Remove o arquivo SQLite antigo, se existir
if os.path.exists('usuarios.db'):
    os.remove('usuarios.db')

# Conexão com SQL Server
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

# Conexão com SQLite
conn_sqlite = sqlite3.connect('usuarios.db')
cursor_sqlite = conn_sqlite.cursor()

# Obter todas as tabelas do banco SQL Server
cursor_sql.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE'
""")
tabelas = [linha[0] for linha in cursor_sql.fetchall()]

# Função para converter valores do tipo Decimal
def converter_linha(linha):
    return [float(valor) if isinstance(valor, Decimal) else valor for valor in linha]

# Dicionário de mapeamento de tipos SQL Server → SQLite
tipo_mapeado = {
    'int': 'INTEGER',
    'bigint': 'INTEGER',
    'smallint': 'INTEGER',
    'tinyint': 'INTEGER',
    'bit': 'INTEGER',
    'nvarchar': 'TEXT',
    'varchar': 'TEXT',
    'text': 'TEXT',
    'ntext': 'TEXT',
    'char': 'TEXT',
    'nchar': 'TEXT',
    'datetime': 'TEXT',
    'date': 'TEXT',
    'float': 'REAL',
    'real': 'REAL',
    'decimal': 'REAL',
    'numeric': 'REAL',
    'money': 'REAL',
    'smallmoney': 'REAL'
}

# Para cada tabela...
for tabela in tabelas:
    print(f'Migrando tabela: {tabela}')

    # Obter colunas da tabela
    cursor_sql.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{tabela}'
    """)
    colunas_info = cursor_sql.fetchall()

    # Criar declaração da tabela em SQLite
    colunas_sqlite = []
    for nome, tipo in colunas_info:
        tipo_sqlite = tipo_mapeado.get(tipo, 'TEXT')  # padrão: TEXT
        colunas_sqlite.append(f'"{nome}" {tipo_sqlite}')
    declaracao_criacao = f'CREATE TABLE IF NOT EXISTS "{tabela}" ({", ".join(colunas_sqlite)})'
    cursor_sqlite.execute(declaracao_criacao)

    # Copiar dados
    colunas = [col[0] for col in colunas_info]
    cursor_sql.execute(f'SELECT {", ".join(colunas)} FROM {tabela}')
    linhas = cursor_sql.fetchall()
    if linhas:
        placeholders = ', '.join(['?'] * len(colunas))
        linhas_convertidas = [converter_linha(linha) for linha in linhas]
        cursor_sqlite.executemany(
            f'INSERT INTO "{tabela}" ({", ".join(colunas)}) VALUES ({placeholders})',
            linhas_convertidas
        )

# Finalizar conexões
conn_sqlite.commit()
conn_sqlite.close()
conn_sql.close()

print("Migração concluída com sucesso!")
