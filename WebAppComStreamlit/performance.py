from db import conectar_banco

def atualizar_desempenho(usuario_id, topico, acertou, dificuldade):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    peso = {"easy": 1, "medium": 2, "hard": 3}[dificuldade]

    if acertou:
        cursor.execute('''
            INSERT INTO desempenho (usuario_id, topico, acertos, erros)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(usuario_id, topico)
            DO UPDATE SET acertos = acertos + excluded.acertos
        ''', (usuario_id, topico, peso, 0))
    else:
        cursor.execute('''
            INSERT INTO desempenho (usuario_id, topico, acertos, erros)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(usuario_id, topico)
            DO UPDATE SET erros = erros + excluded.erros
        ''', (usuario_id, topico, 0, peso))

    conexao.commit()
    conexao.close()

def recuperar_desempenho(usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT topico, acertos, erros FROM desempenho WHERE usuario_id = ?', (usuario_id,))
    desempenho = cursor.fetchall()
    conexao.close()

    return {topico: {"acertos": acertos, "erros": erros} for topico, acertos, erros in desempenho}

def aplicar_decaimento(usuario_id, taxa_decaimento=0.01):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        UPDATE desempenho
        SET acertos = acertos * (1 - ?),
            erros = erros * (1 - ?)
        WHERE usuario_id = ?
    ''', (taxa_decaimento, taxa_decaimento, usuario_id))

    conexao.commit()
    conexao.close()
