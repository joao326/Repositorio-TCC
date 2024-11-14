import streamlit as st
from Prova import Prova 
#import random

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

# Inicializar a prova e gerar perguntas
prova = Prova('perguntas.json', questoes_por_topico)
prova.gerar_prova()

# Ativando session_state
ss = st.session_state
# Inicializando session_states
if "questao_atual" not in ss:
    ss.questao_atual = 0
    ss.pontuacao = 0
    ss.resultados = []

def exibir_questao():
    if ss.questao_atual < len(prova.prova):
        questao = prova.prova[ss.questao_atual]
        print(questao)
        st.write(f"Questão {ss.questao_atual + 1}: {questao['question']}")
        
        # Exibição das opções
        escolha = st.radio("Escolha uma resposta:", questao['options'], index=None, key=f"questao_{ss.questao_atual}") 
        # key=ss.questao_atual - id. cada componente(cada opção) de forma única

        # Exibição das variáveis session_state
        st.write(ss)

        if questao == 'a':
            st.write("Você selecionou a alternativa a")

        "before pressing button", ss.questao_atual
        if st.button('Confirmar', key=f"confirmar_{ss.questao_atual}"):
            if escolha:
                if escolha == questao['answer']:
                    st.success("Correto!")
                    ss.pontuacao +=1
                    ss.resultados.append(f"Questão {ss.questao_atual + 1}: Correta")
                else:
                    st.error("Incorreto!")
                    ss.resultados.append(
                        f"Questão {ss.questao_atual + 1}: Incorreta - Resposta correta: {questao['answer']}"
                    )
            ss.questao_atual += 1
            "after pressing button", ss.questao_atual

    else:
        st.write("Prova concluída!")
        st.write(f"Sua pontuação final: {ss.pontuacao} de {len(prova.prova)}")
        st.write("Resultados detalhados:")
        for resultado in ss.resultados:
            st.write(resultado)
        st.stop()

# Caractere de nova linha
def nl ( num_de_linhas ):
    for i in range(num_de_linhas):
        st.write(" ")

st.header("Prova de Java")
nl(1)
st.markdown("""
            Write Quiz Description and Instructions.
            """)
scorecard_placeholder = st.empty()
# Executar a função para exibir a questão atual
exibir_questao()