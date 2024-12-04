def registrar_resposta(desempenho_usuario, topico, acertou, dificuldade): # em verificar resposta
    peso = {"easy": 1, "medium": 2, "hard": 3}[dificuldade]
    if acertou:
        desempenho_usuario[topico]["acertos"] += peso
    else:
        desempenho_usuario[topico]["erros"] += peso

def calcular_pfa(desempenho_usuario, alpha=1.0, beta=0.5): # em mostrar resultado
    resultados = {}
    for topico, dados in desempenho_usuario.items():
        acertos = dados["acertos"]
        erros = dados["erros"]
        resultados[topico] = max(0, alpha * acertos - beta * erros)  # Garante não negativo
    return resultados

def gerar_feedback_final(pfa_resultados, limite_baixo=5, limite_medio=10): # em mostrar resultado
    feedback = {"prioridade": [], "adequado": [], "excelente": []}
    for topico, desempenho in pfa_resultados.items():
        if desempenho < limite_baixo:
            feedback["prioridade"].append(topico)
        elif desempenho < limite_medio:
            feedback["adequado"].append(topico)
        else:
            feedback["excelente"].append(topico)
    return feedback
