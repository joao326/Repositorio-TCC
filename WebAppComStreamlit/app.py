import streamlit as st
from Prova import Prova
from pfa import registrar_resposta, calcular_pfa, gerar_feedback_final

# Streamlit é stateless; usamos session_state para persistir os dados
ss = st.session_state

# Dicionário com o total de questões por tópico (não alterado)
questoes_por_topico_total = {  # total = 101
    "Basic Syntax": 11,
    "DataTypes, Variables": 11,
    "Conditionals": 9,
    "Functions": 11,
    "Loops": 8,
    "Exception Handling": 12,
    "DataStructures": 6,
    "OOP, Interfaces, Classes": 10,
    "Packages": 12,
    "Working With Files and APIs": 11,
}

def ajustar_questoes_por_topico(num_questoes):
    """
    Calcula o número de questões por tópico de forma uniforme,
    com base no número total de questões escolhido.
    """
    questoes_por_topico = {}
    num_topicos = len(questoes_por_topico_total)
    num_questoes_por_topico = num_questoes // num_topicos
    for topico in questoes_por_topico_total:
        questoes_por_topico[topico] = num_questoes_por_topico
    return questoes_por_topico

def inicializar_ss():
    """
    Inicializa as variáveis no session_state se ainda não existirem.
    """
    if 'start' not in ss:
        ss['start'] = False
    if 'current_question' not in ss:
        ss['current_question'] = 0
    if 'user_answers' not in ss:
        ss['user_answers'] = []
    if 'score' not in ss:
        ss['score'] = 0
    if 'feedback' not in ss:
        ss['feedback'] = False
    if 'desempenho_usuario' not in ss:
        ss['desempenho_usuario'] = {}
    if 'prova' not in ss:
        ss['prova'] = []
    if 'questoes_por_topico' not in ss:
        ss['questoes_por_topico'] = {}
    if 'total_de_questoes' not in ss:
        ss['total_de_questoes'] = 0

inicializar_ss()

def atualizar_ss():
    """
    Atualiza o session_state após o usuário iniciar a prova.
    Calcula a distribuição de questões, define o total de questões
    e gera a prova.
    """
    # Recalcula a distribuição de questões com base no valor selecionado pelo usuário
    questoes_por_topico = ajustar_questoes_por_topico(ss['num_questoes'])
    ss['questoes_por_topico'] = questoes_por_topico
    ss['total_de_questoes'] = sum(questoes_por_topico.values())

    ss['start'] = True

    # Cria a prova com base no arquivo e na distribuição de questões
    prova_obj = Prova('perguntasT.json', questoes_por_topico)
    prova_obj.gerar_prova()
    ss['prova'] = prova_obj.prova

    # Reinicia as variáveis de controle
    ss['current_question'] = 0
    ss['user_answers'] = []
    ss['score'] = 0
    ss['desempenho_usuario'] = {
        topico: {"acertos": {"easy": 0, "medium": 0, "hard": 0},
                 "erros": {"easy": 0, "medium": 0, "hard": 0}}
        for topico in questoes_por_topico
    }

def mostrar_pergunta():
    """
    Exibe a pergunta atual e retorna a escolha do usuário.
    """
    current_question = ss['current_question']
    question = ss['prova'][current_question]
    st.header(f"Pergunta {current_question + 1}")
    st.write(f"Tópico: {question['topic']}")
    st.write(question['question'])
    options = question['options']
    user_choice = st.radio("Escolha uma resposta:", options, index=None, key=f"question_{current_question}")
    return user_choice

def verificar_resposta(user_choice):
    """
    Verifica se a resposta do usuário está correta e atualiza
    o desempenho e a pontuação.
    """
    current_question = ss['current_question']
    question = ss['prova'][current_question]

    if user_choice is None:
        st.error("Por favor, selecione uma resposta antes de avançar.")
        return

    dificuldade = question.get("difficulty", "medium")  # 'medium' como padrão
    acertou = user_choice.strip() == question['answer'].strip()
    registrar_resposta(ss['desempenho_usuario'], question['topic'], acertou, dificuldade)

    if acertou:
        st.success("Correto!")
        ss['score'] += 1
    else:
        st.error(f"Incorreto! Resposta correta: {question['answer']}")
    ss['user_answers'].append(user_choice)
    ss['feedback'] = True

def proxima_pergunta():
    """
    Avança para a próxima pergunta e reinicia o feedback.
    """
    ss['current_question'] += 1
    ss['feedback'] = False    
    st.rerun()  # Use st.rerun() se preferir

def mostrar_resultado():
    """
    Exibe o resultado final, a pontuação por tópico e o feedback do desempenho.
    """
    st.write("## Resultado Final")
    st.write(f"Você acertou {ss['score']} de {ss['total_de_questoes']} perguntas!")

    pfa_resultados = calcular_pfa(ss['desempenho_usuario'])
    feedback = gerar_feedback_final(
        {topico: resultado["p"] for topico, resultado in pfa_resultados.items()},
        ss['total_de_questoes']
    )

    st.write("### Pontuação por Tópico:")
    for topico, resultados in pfa_resultados.items():
        nota = round(resultados["p"] * 10, 2)  # Multiplica p por 10 e arredonda
        st.write(f"- **{topico}**: {nota} / 10")

    st.write("### Feedback do seu desempenho:")
    st.write("#### Prioridade para estudo:")
    st.write(", ".join(feedback['prioridade']) or "Nenhum")
    st.write("#### Adequado:")
    st.write(", ".join(feedback['adequado']) or "Nenhum")
    st.write("#### Excelente:")
    st.write(", ".join(feedback['excelente']) or "Nenhum")

    if st.button("Reiniciar Quiz"):
        ss.clear()
        st.rerun()

def gerenciar_prova():
    """
    Controla o fluxo da prova: mostra a pergunta, verifica a resposta
    e, ao terminar todas as questões, exibe o resultado final.
    """
    if not ss['start']:
        return  # Se a prova não foi iniciada, não faz nada

    if ss['current_question'] < ss['total_de_questoes']:
        st.write(f"Progresso: {ss['current_question'] + 1} / {ss['total_de_questoes']}")
        user_choice = mostrar_pergunta()

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Verificar Resposta", key=f"verificar_{ss['current_question']}"):
                verificar_resposta(user_choice)
        with col2:
            if ss['feedback']:
                if st.button("Próxima Pergunta", key=f"proxima_{ss['current_question']}"):
                    proxima_pergunta()
    else:
        mostrar_resultado()

# Interface inicial (configurações da prova)
if not ss['start']:
    st.title("GAP.AI")
    st.write("Bem vindo! Descubra suas lacunas de aprendizado e saiba qual conteúdo estudar para aprender de maneira mais eficiente!")
    st.header("Configurações da Prova")
    # Aqui o usuário escolhe a quantidade de questões desejada
    ss['num_questoes'] = st.radio(
        "Escolha a quantidade de questões (quanto mais questões, mais exato é o resultado):",
        options=[10, 30, 40, 50, 60],
    )
    if st.button("Iniciar Prova"):
        atualizar_ss()
        st.rerun()

# Gerencia a exibição da prova
gerenciar_prova()
