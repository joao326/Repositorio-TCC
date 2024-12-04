import streamlit as st 
import time
from Prova import Prova
from pfa import registrar_resposta, calcular_pfa, gerar_feedback_final

# Streamlit é stateless
# Stateless: código é reexecutado a cada interação do usuário
# Variáveis normais são reinicializadas, mas session states não

scorecard_placeholder = st.empty()

# Definição da quantidade questões
questoes_por_topico = {
    "Basic Syntax": 11,
    "DataTypes, Variables": 11,
    "Conditionals": 9,
    "Functions": 11,
    "Loops": 8,
    "Exception Handling": 12,
    "DataStructures": 6,
    "OOP, Interfaces, Classes": 10,
    "Packages": 12,
    "Working With Files and APIs": 11
}
total_de_questoes = sum(questoes_por_topico.values())

# ss armazena e gerencia estados de variáveis entre interações do usuário
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
        prova = Prova('perguntasT.json', questoes_por_topico)
        prova.gerar_prova()
        ss['prova'] = prova.prova
        ss['current_question'] = 0
        ss['user_answers'] = []
        ss['score'] = 0
    elif ss.counter == 2:
        ss['stop'] = True

#st.write("# GAP.AI")
if ss['counter'] == 0:
    st.title("GAP.AI")
    #st.subheader("Bem vindo!")
    st.write("Bem vindo! Descubra suas lacunas de aprendizado e saiba qual conteúdo estudar para aprender de maneira mais eficiente!")
    st.write("Clique no botão abaixo para iniciar a prova.")

col3, col4 = st.columns([1,1.25])
# Inicializando botão
with col3:
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

    # Verifica se usuário selecionou resposta
    if user_choice is None:
        st.error("Por favor, selecione uma questão antes de avançar.")
        return # Interrompe execução da função caso sem escolha

    if user_choice.strip() == question['answer'].strip():
        st.success("Correto!")
        ss['score'] += 1
    else:
        st.error(f"Incorreto! Resposta correta: {question['answer']}")
    ss['user_answers'].append(user_choice)
    ss['feedback'] = True

def proxima_pergunta():
    ss['current_question'] += 1
    ss['feedback'] = False

def mostrar_resultado():
    st.write("## Resultado Final")
    st.write(f"Você acertou {ss['score']} de {total_de_questoes} perguntas!")
    if st.button("Reiniciar Quiz"):
        ss['counter'] = 0 # ?
        ss.clear()   
        st.rerun() 

def gerenciar_questao():
    # if do processo de resolução da prova
    if ss['start'] and ss['current_question'] < total_de_questoes:
        with col4:
            st.write(f"Progresso: {ss['current_question'] + 1} / {total_de_questoes}")
        user_choice = mostrar_pergunta()

        #ss['user_choice'] = user_choice

        # Criação de colunas para botões a seguir
        col1, col2 = st.columns([1,2])
        
        with col1:
            if st.button("Verificar Resposta", key=f"verificar_{ss['current_question']}"):
                verificar_resposta(user_choice)

        with col2:        
            if ss['feedback']:  # Caso ainda não tenha mostrado o feedback
                if st.button("Próxima Pergunta", key=f"proxima_{ss['current_question']}"):
                    proxima_pergunta()
                    st.rerun()

    # Mostrar resultado ao finalizar
    elif ss['current_question'] >= total_de_questoes:
        mostrar_resultado()
gerenciar_questao()
