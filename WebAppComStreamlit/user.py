from db import conectar_banco
import sqlite3

def registrar_usuario(nome, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
        conexao.commit()
        print("Usuário registrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Usuário já registrado!")
    finally:
        conexao.close()

def autenticar_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
    usuario = cursor.fetchone()
    conexao.close()

    if usuario:
        return usuario[0]
    else:
        return None