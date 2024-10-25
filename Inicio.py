import streamlit as st
import time
import random

# # Script para atualização contínua da página
# # Função para gerar e mostrar um número aleatório
# def print_random_number():
#     random_number = random.randint(1, 100)
#     st.write(f"Número aleatório gerado: {random_number}")

# # Inicializa a contagem de tempo
# if 'last_run' not in st.session_state:
#     st.session_state['last_run'] = time.time()

# # Espaço reservado para atualizar o número
# placeholder = st.empty()

# # Loop para atualizar a cada 10 segundos sem bloquear o Streamlit
# while True:
#     current_time = time.time()
#     time_since_last_run = current_time - st.session_state['last_run']
    
#     if time_since_last_run >= 10:  # 10 segundos
#         with placeholder.container():
#             print_random_number()
#         st.session_state['last_run'] = current_time
    
#     # Pequena pausa para evitar consumo excessivo de CPU
#     time.sleep(1)

st.set_page_config(page_title="Dashboard de Indicadores de Aprendizagem")

st.sidebar.image("./icons/logoEAD.png", width=150)

st.title("Receba as boas-vindas ao Dashboard de Indicadores de Apredizagem")
st.write("Use o menu lateral para navegar entre as disciplinas da Graduação EaD, Graduação Presencial e os Grupos de Trabalho")