import streamlit as st
from Prova import Prova
from pfa import registrar_resposta, calcular_pfa, gerar_feedback_final
from database import conectar_banco, criar_tabelas, registrar_usuario, atualizar_desempenho, recuperar_desempenho, aplicar_decaimento

# Streamlit é stateless; usamos session_state para persistência
ss = st.session_state

# Criar tabelas no banco de dados ao iniciar
criar_tabelas()

# Função para autenticação do usuário
def autenticar_usuario():
    st.title("Autenticação")
    st.write("Registre-se ou faça login para começar.")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    
    if st.button("Entrar"):
        if nome and email:
            # Registrar ou autenticar o usuário
            registrar_usuario(nome, email)
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            usuario = cursor.fetchone()
            conexao.close()
            
            if usuario:
                ss['usuario_id'] = usuario[0]
                st.success(f"Bem-vindo, {nome}!")
                aplicar_decaimento(ss['usuario_id'])  # Aplica decaimento ao desempenho
                ss['start'] = False  # Permite iniciar a prova
                st.experimental_rerun()
            else:
                st.error("Erro ao autenticar usuário.")
        else:
            st.error("Por favor, insira nome e email.")

# Interface para configurar a prova
def configurar_prova():
    st.title("GAP.AI")
    st.write("Bem-vindo! Descubra suas lacunas de aprendizado e saiba qual conteúdo estudar de maneira mais eficiente!")
    st.header("Configurações da Prova")
    ss['num_questoes'] = st.radio(
        "Escolha a quantidade de questões (quanto mais questões, mais exato é o resultado):",
        options=[10, 30, 40, 50, 60],
        index=0
    )
    if st.button("Iniciar Prova"):
        atualizar_ss()
        st.rerun()

# Atualizar session_state para nova prova
def atualizar_ss():
    ss['start'] = True
    prova = Prova('perguntasT.json', questoes_por_topico)
    prova.gerar_prova()
    ss['prova'] = prova.prova
    ss['current_question'] = 0
    ss['user_answers'] = []
    ss['score'] = 0
    ss['desempenho_usuario'] = {topico: {"acertos": 0, "erros": 0} for topico in questoes_por_topico}

# Verificar resposta e atualizar desempenho no banco
def verificar_resposta(user_choice):
    current_question = ss['current_question']
    question = ss['prova'][current_question]
    if user_choice is None:
        st.error("Por favor, selecione uma resposta antes de avançar.")
        return

    dificuldade = question.get("difficulty", "medium")
    acertou = user_choice.strip() == question['answer'].strip()
    registrar_resposta(ss['desempenho_usuario'], question['topic'], acertou, dificuldade)
    
    # Atualizar banco de dados
    atualizar_desempenho(ss['usuario_id'], question['topic'], acertou, dificuldade)

    # Feedback para o usuário
    if acertou:
        st.success("Correto!")
        ss['score'] += 1
    else:
        st.error(f"Incorreto! Resposta correta: {question['answer']}")
    ss['user_answers'].append(user_choice)
    ss['feedback'] = True

# Mostrar resultado e feedback final
def mostrar_resultado():
    st.write("## Resultado Final")
    st.write(f"Você acertou {ss['score']} de {total_de_questoes} perguntas!")

    # Recuperar desempenho atualizado
    desempenho = recuperar_desempenho(ss['usuario_id'])
    desempenho_dict = {topico: {"acertos": dados[1], "erros": dados[2]} for topico, *dados in desempenho}

    pfa_resultados = calcular_pfa(desempenho_dict)
    feedback = gerar_feedback_final(pfa_resultados, total_de_questoes)

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

# Fluxo principal
if 'usuario_id' not in ss:
    autenticar_usuario()
elif not ss.get('start', False):
    configurar_prova()
else:
    gerenciar_prova()
