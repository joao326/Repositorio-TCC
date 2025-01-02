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
    peso = {"easy": 1, "medium": 2, "hard": 3}[dificuldade]
    if acertou:
        desempenho_usuario[topico]["acertos"] += peso
    else:
        desempenho_usuario[topico]["erros"] += peso

def calcular_pfa(desempenho_usuario, alpha=1.0, beta=0.5):
    """
    Calcula o PFA (Performance Feedback Assessment) para cada tópico com base no desempenho do usuário.

    Args:
        desempenho_usuario (dict): Dicionário contendo o desempenho do usuário por tópico.
        alpha (float): Peso para acertos.
        beta (float): Peso para erros.

    Returns:
        dict: Dicionário com o PFA calculado para cada tópico.
    """
    resultados = {}
    for topico, dados in desempenho_usuario.items():
        acertos = dados["acertos"]
        erros = dados["erros"]
        resultados[topico] = max(0, alpha * acertos - beta * erros)  # Garante não negativo
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
