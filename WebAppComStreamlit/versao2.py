import streamlit as st
from Prova import Prova 
#import random
import time

scorecard_placeholder = st.empty()

# Configurações para a prova
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

# Inicializar a prova e gerar perguntas
prova = Prova('perguntas.json', questoes_por_topico)
prova.gerar_prova()


# Ativando session_state
ss = st.session_state
# Inicializando session_states
#if "questao_atual" not in ss:
    #ss.questao_atual = 0
    #ss.pontuacao = 0
    #ss.resultados = []

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
if 'current_quiz' not in ss:
    ss['current_quiz'] = {}
if 'user_answers' not in ss:
    ss['user_answers'] = []
if 'grade' not in ss:
    ss['grade'] = 0

# Caractere de nova linha
def nl ( num_de_linhas ):
    for i in range(num_de_linhas):
        st.write(" ")

# Function for button click
def btn_click():
    ss.counter += 1
    if ss.counter > 2: 
        ss.counter = 0
        ss.clear()
    else:
        update_session_state()
        with st.spinner("*this may take a while*"):
            time.sleep(2)

# Function to update current session
def update_session_state():
    if ss.counter == 1:
        ss['start'] = True
        prova = Prova('perguntas.json', questoes_por_topico)
        prova.gerar_prova()
        ss.current_test = prova
    elif ss.counter == 2:
        # Set start to False
        ss['start'] = True
        # Set stop to True
        ss['stop'] = True

# Initializing Button Text
st.button(label=ss.button_label[ss.counter], 
        key='button_press', on_click= btn_click)

def exibir_questao():
    with st.container():
        if(ss.start):
            for i in range(total_de_questoes+1):
                number_placeholder = st.empty()
                question_placeholder = st.empty()
                options_placeholder = st.empty()
                results_placeholder = st.empty()
                expander_area = st.empty()
                

                current_question = i+1
                number_placeholder.write(f"Question {current_question}*")
                question_placeholder.write(f"**{ss.current_test[i].get('question')}**")
                options = ss.current_test[i].get("options")
                options_placeholder.radio("",options, index=1,key=f"Q{current_question}")
                nl(1)

                #Grade answers and return corrections
                if ss.stop:
                    # Track length of user_answers
                    if len(ss.user_answers) < total_de_questoes:
                        # comparing answers to track score
                        if ss[f'Q{current_question}'] == ss.current_test[i].get("correct_answer"):
                            ss.user_answers.append(True)
                        else:
                            pass
                        if ss.user_answer[i]==True:
                            results_placeholder.sucess("CORRECT")
                        else:
                            results_placeholder.error("INCORRECT")
                        expander_area.write(f"*{ss.current_test[i].get('explanation')}*")
    if ss.stop:
        ss['grade'] == ss.user_answer.count(True)
        scorecard_placeholder.write(f"### **Your Final Score : {ss['grade']} / {len(ss.current_test)}**")   

exibir_questao()