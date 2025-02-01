import streamlit as st
from Prova import Prova
from pfa import registrar_resposta, calcular_pfa, gerar_feedback_final
from user import registrar_usuario, autenticar_usuario
from performance import atualizar_desempenho, recuperar_desempenho, aplicar_decaimento
from db import criar_tabelas

# Cria as tabelas no banco de dados
criar_tabelas()

# Streamlit é stateless; variáveis persistem no session_state
ss = st.session_state

if 'num_questoes' not in ss:
    ss['num_questoes'] = 0  # Valor padrão
# Autenticação
if 'usuario_id' not in ss:
    st.title("Autenticação")
    email = st.text_input("Email")
    nome = st.text_input("Nome (apenas para novos usuários)")

    if st.button("Entrar"):
        usuario_id = autenticar_usuario(email)
        if not usuario_id:
            if nome:
                registrar_usuario(nome, email)
                usuario_id = autenticar_usuario(email)
                st.success("Usuário registrado com sucesso!")
            else:
                st.error("Usuário não encontrado. Forneça um nome para se registrar.")
        if usuario_id:
            ss['usuario_id'] = usuario_id
            st.rerun()
        else:
            st.error("Erro ao autenticar. Tente novamente.")
if 'usuario_id' in ss:
    aplicar_decaimento(ss['usuario_id'])

def ajustar_questoes_por_topico(num_questoes):
    # Calcula o número de questões por tópico com base na quantidade total selecionada
    questoes_por_topico = {}
    num_questoes_por_topico = num_questoes // len(questoes_por_topico_total) # ?
    
    for topico in questoes_por_topico_total:
        questoes_por_topico[topico] = num_questoes_por_topico
    
    return questoes_por_topico

questoes_por_topico_total = { # total = 101
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

# Ajusta o dicionário de acordo com a escolha do usuário
questoes_por_topico = ajustar_questoes_por_topico(ss['num_questoes'])
total_de_questoes = sum(questoes_por_topico.values())

def inicializar_ss():
    if 'counter' not in ss:
        ss['counter'] = 0
    if 'start' not in ss:
        ss['start'] = False
    if 'stop' not in ss:
        ss['stop'] = False
    if 'prova' not in ss:
        prova = Prova('perguntasT.json', questoes_por_topico)
        prova.gerar_prova()
        ss['prova'] = prova.prova
    if 'current_question' not in ss:
        ss['current_question'] = 0
    if 'user_answers' not in ss:
        ss['user_answers'] = []
    if 'score' not in ss:
        ss['score'] = 0

    if 'feedback' not in ss:
        ss['feedback'] = False

    if 'usuario_id' in ss:
        desempenho = recuperar_desempenho(ss['usuario_id'])
        ss['desempenho_usuario'] = desempenho
    else:
        ss['desempenho_usuario'] = {
            topico: {"acertos": {"easy": 0, "medium": 0, "hard": 0}, 
                                "erros": {"easy": 0, "medium": 0, "hard": 0}}
            for topico in questoes_por_topico
        }


inicializar_ss()

def atualizar_ss():
    ss['start'] = True
    prova = Prova('perguntasT.json', questoes_por_topico)
    prova.gerar_prova()
    ss['prova'] = prova.prova
    ss['current_question'] = 0
    ss['user_answers'] = []
    ss['score'] = 0
    ss['desempenho_usuario'] = {
        topico: {"acertos": {"easy": 0, "medium": 0, "hard": 0}, 
                             "erros": {"easy": 0, "medium": 0, "hard": 0}}
        for topico in questoes_por_topico
    }

def mostrar_pergunta():
    current_question = ss['current_question']
    question = ss['prova'][current_question]
    st.header(f"Pergunta {current_question + 1}")
    st.write(f"Tópico: {question['topic']}")
    st.write(question['question'])
    options = question['options']
    user_choice = st.radio("Escolha uma resposta:", options, index=None, key=f"question_{current_question}")
    return user_choice

# registrar no PFA
def verificar_resposta(user_choice):
    current_question = ss['current_question']
    question = ss['prova'][current_question]

    if user_choice is None:
        st.error("Por favor, selecione uma questão antes de avançar.")
        return

    dificuldade = question.get("difficulty", "medium")  # 'medium' como padrão
    acertou = user_choice.strip() == question['answer'].strip()

    # Atualiza o desempenho no PFA local
    registrar_resposta(ss['desempenho_usuario'], question['topic'], acertou, dificuldade)

    # Atualiza o desempenho no banco de dados
    usuario_id = ss['usuario_id']
    atualizar_desempenho(usuario_id, question['topic'], acertou, dificuldade)

    if acertou:
        st.success("Correto!")
        ss['score'] += 1
    else:
        st.error(f"Incorreto! Resposta correta: {question['answer']}")
    ss['user_answers'].append(user_choice)
    ss['feedback'] = True


def proxima_pergunta():
    ss['current_question'] += 1
    ss['feedback'] = False    
    st.rerun() # use it instead of st.experimental_rerun()

def mostrar_resultado():
    st.write("## Resultado Final")
    st.write(f"Você acertou {ss['score']} de {total_de_questoes} perguntas!")

    pfa_resultados = calcular_pfa(ss['desempenho_usuario'])

    feedback = gerar_feedback_final({topico: resultado["p"] for topico, resultado in pfa_resultados.items()}, total_de_questoes)

    # Exibe a pontuação por tópico
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

    # Info do bd
    usuario_id = ss['usuario_id']
    desempenho_atualizado = recuperar_desempenho(usuario_id)

    st.write("### Desempenho por Tópico:")
    for topico, dados in desempenho_atualizado.items():
        acertos = dados["acertos"]
        erros = dados["erros"]
        st.write(f"- **{topico}**: Acertos: {acertos}, Erros: {erros}")

    if st.button("Reiniciar Quiz"):
        ss.clear()
        st.rerun()

def gerenciar_prova():
    if ss['start'] and ss['current_question'] < total_de_questoes:
        st.write(f"Progresso: {ss['current_question'] + 1} / {total_de_questoes}")
        user_choice = mostrar_pergunta()

        col1, col2 = st.columns([1,2])
        
        with col1:
            if st.button("Verificar Resposta", key=f"verificar_{ss['current_question']}"):
                verificar_resposta(user_choice)

        with col2:        
            if ss['feedback']:
                if st.button("Próxima Pergunta", key=f"proxima_{ss['current_question']}"):
                    proxima_pergunta()
    elif ss['current_question'] >= total_de_questoes:
        mostrar_resultado()

# Interface inicial
if not ss['start']:
    st.title("GAP.AI")
    st.write("Bem vindo! Descubra suas lacunas de aprendizado e saiba qual conteúdo estudar para aprender de maneira mais eficiente!")
    st.header("Configurações da Prova")
    ss['num_questoes'] = st.radio(
        "Escolha a quantidade de questões(quanto mais questões mais exato é o resultado):",
        options=[10,30, 40, 50, 60],
        index=0  # Seleciona 30 como padrão (Precisa mesmo?)
    )
    if st.button("Iniciar Prova"):
        atualizar_ss()
        st.rerun()

gerenciar_prova()