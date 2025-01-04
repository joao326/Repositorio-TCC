import sqlite3

def conectar_banco():
    return sqlite3.connect('usuarios.db')

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Tabela para armazenar usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabela para armazenar desempenho por tópico
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS desempenho (
            usuario_id INTEGER,
            topico TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            PRIMARY KEY (usuario_id, topico)
        )
    ''')

    conexao.commit()
    conexao.close()