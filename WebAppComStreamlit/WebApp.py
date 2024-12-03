import streamlit as st
from Prova import Prova
import time

scorecard_placeholder = st.empty()

# Definição da quantidade questões
questoes_por_topico = {
    "Basic Syntax": 1,
    "DataTypes, Variables": 1,
    "Conditionals": 1,
    "Functions": 0,
    "Loops": 0,
    "Exception Handling": 0,
    "DataStructures": 0,
    "OOP, Interfaces, Classes": 0,
    "Packages": 0,
    "Working With Files and APIs": 0
}
total_de_questoes = sum(questoes_por_topico.values())

# Apelidando session_state
ss = st.session_state

# Inicializando session_states
if 'counter' not in ss:
    ss['counter'] = 0
if 'start' not in ss:
    ss['start'] = False
if 'stop' not in ss:
    ss['stop'] = False
if 'refresh' not in ss:
    ss['refresh'] = False
if "button_label" not in ss:
    ss['button_label'] = ['START', 'SUBMIT', 'RELOAD']
if 'prova' not in ss:
    prova = Prova('perguntas.json', questoes_por_topico)
    prova.gerar_prova()
    ss['prova'] = prova.prova
if 'current_question' not in ss:
    ss['current_question'] = 0
if 'user_answers' not in ss:
    ss['user_answers'] = []
if 'score' not in ss:
    ss['score'] = 0

# Caractere de nova linha
def new_line(num_de_linhas):
    for i in range(num_de_linhas):
        st.write(" ")

# Função para click em botões
def btn_click():
    ss.counter += 1
    if ss.counter > 2: # Apenas um click por ação
        ss.counter = 0
        ss.clear()
    else:
        update_session_state()
        with st.spinner("*Espere um segundo...*"):
            time.sleep(2)

# Atualizar sessão atual
def update_session_state():
    if ss.counter == 1:
        ss['start'] = True
        prova = Prova('perguntas.json', questoes_por_topico)
        prova.gerar_prova()
        ss['prova'] = prova.prova
        ss['current_question'] = 0
        ss['user_answers'] = []
        ss['score'] = 0
    elif ss.counter == 2:
        ss['stop'] = True

# Inicializando botão
st.button(label=ss.button_label[ss.counter], key='button_press', on_click=btn_click)

def mostrar_pergunta():
    current_question = ss['current_question']
    question = ss['prova'][current_question]

    st.header(f"Pergunta {current_question + 1}")
    st.write(question['question'])

    options = question['options']
    user_choice = st.radio("Escolha uma resposta:", options, index=None, key=f"question_{current_question}")
    return user_choice

def verificar_resposta(user_choice):
    current_question = ss['current_question']
    question = ss['prova'][current_question]

    if user_choice.strip() == question['answer'].strip():
        st.success("Resposta Correta!")
        ss['score'] += 1
    else:
        st.error(f"Resposta Incorreta! A resposta correta é: {question['answer']}")
    ss['user_answers'].append(user_choice)
    ss['current_question'] += 1

def mostrar_resultado():
    st.write("## Resultado Final")
    st.write(f"Você acertou {ss['score']} de {total_de_questoes} perguntas!")
    if st.button("Reiniciar Quiz"):
        ss['counter'] = 0
        ss.clear()    

def gerenciar_questao():
    if ss['start'] and ss['current_question'] < total_de_questoes:
        user_choice = mostrar_pergunta()
        if st.button("Verificar Resposta", key=f"verificar_{ss['current_question']}"):
            verificar_resposta(user_choice)

    elif ss['current_question'] >= total_de_questoes:
        mostrar_resultado()
gerenciar_questao()