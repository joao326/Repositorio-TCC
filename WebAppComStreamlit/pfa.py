import math

def registrar_resposta(desempenho_usuario, topico, acertou, dificuldade):
    """
    Registra a resposta do usuário atualizando seu desempenho no tópico especificado.

    Args:
        desempenho_usuario (dict): Dicionário contendo o desempenho do usuário por tópico.
        topico (str): O tópico da questão respondida.
        acertou (bool): Indicador se o usuário acertou a questão.
        dificuldade (str): A dificuldade da questão ('easy', 'medium', 'hard').

    Returns:
        None
    """
    if topico not in desempenho_usuario:
        desempenho_usuario[topico] = {"acertos": {"easy": 0, "medium": 0, "hard": 0}, "erros": {"easy": 0, "medium": 0, "hard": 0}}

    if acertou:
        desempenho_usuario[topico]["acertos"][dificuldade] += 1
    else:
        desempenho_usuario[topico]["erros"][dificuldade] += 1

def calcular_pfa(desempenho_usuario):
    """
    Calcula o desempenho bruto (m) e a probabilidade (p) para cada tópico com base no desempenho do usuário.

    Args:
        desempenho_usuario (dict): Dicionário contendo o desempenho do usuário por tópico.

    Returns:
        dict: Dicionário com a pontuação (p) para cada tópico.
    """
    # Pesos para acertos e erros conforme a dificuldade
    pesos_acerto = {"easy": 0.993, "medium": 1.194, "hard": 1.386}
    pesos_erro = {"easy": 0.5, "medium": 0.6, "hard": 0.8}

    resultados = {}
    for topico, dados in desempenho_usuario.items():
        acertos = dados["acertos"]
        erros = dados["erros"]

        # Calcula o desempenho bruto (m)
        desempenho_bruto = sum(
            acertos[dificuldade] * pesos_acerto[dificuldade] -
            erros[dificuldade] * pesos_erro[dificuldade]
            for dificuldade in ["easy", "medium", "hard"]
        )

        # Calcula a probabilidade (p) usando a função logística
        probabilidade = 1 / (1 + math.exp(-desempenho_bruto))

        # Armazena os resultados
        resultados[topico] = {
            "m": desempenho_bruto,
            "p": probabilidade
        }

    return resultados

def gerar_feedback_final(pfa_resultados, total_questoes, limite_baixo_ratio=0.1, limite_medio_ratio=0.2):
    """
    Gera o feedback final com base nos resultados do PFA.

    Args:
        pfa_resultados (dict): Dicionário com os resultados do PFA para cada tópico.
        total_questoes (int): Número total de questões.
        limite_baixo_ratio (float): Razão para calcular o limite inferior.
        limite_medio_ratio (float): Razão para calcular o limite médio.

    Returns:
        dict: Dicionário com o feedback classificado em 'prioridade', 'adequado' e 'excelente'.
    """

    limite_baixo = total_questoes * limite_baixo_ratio
    limite_medio = total_questoes * limite_medio_ratio

    # Calcula os limites com base nos resultados
    feedback = {"prioridade": [], "adequado": [], "excelente": []}
    for topico, desempenho in pfa_resultados.items():
        if desempenho < limite_baixo:
            feedback["prioridade"].append(topico)
        elif desempenho < limite_medio:
            feedback["adequado"].append(topico)
        else:
            feedback["excelente"].append(topico)
    return feedback
