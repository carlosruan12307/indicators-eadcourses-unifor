import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurações globais de estilo para matplotlib
plt.rcParams['figure.facecolor'] = '#0E1117'  # Fundo da figura
plt.rcParams['axes.facecolor'] = '#0E1117'    # Fundo dos eixos
plt.rcParams['savefig.facecolor'] = '#0E1117' # Fundo ao salvar figuras
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

# Carregar os dados do arquivo CSV
file_path = './database.csv'
data = pd.read_csv(file_path)

# Filtrar apenas as disciplinas do Trimestre T1 e usuários com papel "Estudante"
students_data = data[(data['Trimestre'] == 'T1') & (data['Papel'] == 'Estudante')]

# Converter a coluna 'Progresso do estudante' de string para float
students_data['Progresso do estudante'] = students_data['Progresso do estudante'].str.replace('%', '').str.replace(',', '.').astype(float)

# Obter a lista de disciplinas únicas
disciplinas = students_data['Nome completo do curso com link'].unique()

# Criar um menu suspenso para selecionar a disciplina
selected_course = st.selectbox('Escolha uma disciplina:', disciplinas)

# Filtrar os dados com base na disciplina selecionada
course_data = students_data[students_data['Nome completo do curso com link'] == selected_course]

# Função para gerar as métricas por disciplina
def generate_metrics(course_data):
    total_students = course_data.shape[0]
    progress_mean = course_data['Progresso do estudante'].mean()
    zero_progress_count = course_data[course_data['Progresso do estudante'] == 0].shape[0]
    
    # Contar usuários que nunca acessaram a disciplina (valores NaN ou "Nunca")
    never_accessed_count = course_data[
        course_data['Último acesso a disciplina'].isna() | 
        (course_data['Último acesso a disciplina'] == "Nunca")
    ].shape[0]
    
    last_access_count = course_data['Último acesso a disciplina'].value_counts()
    
    return total_students, progress_mean, zero_progress_count, never_accessed_count, last_access_count

# Gerar métricas para a disciplina selecionada
if not course_data.empty:
    total_students, progress_mean, zero_progress_count, never_accessed_count, last_access_count = generate_metrics(course_data)
    
    # Exibir as informações
    st.subheader(f'Disciplina: {selected_course}')
    st.write(f"Quantidade total de estudantes: {total_students}")
    st.write(f"Média do progresso: {progress_mean:.2f}%")
    st.write(f"Quantidade de estudantes com 0% de progresso: {zero_progress_count}")
    st.write(f"Quantidade de estudantes que nunca acessaram a disciplina: {never_accessed_count}")
    
    # Gráfico de Pizza 3D: Estudantes com 0% de progresso
    fig1, ax1 = plt.subplots()
    labels = ['0% de Progresso', 'Outros']
    sizes = [zero_progress_count, total_students - zero_progress_count]
    explode = (0.1, 0)  # "Explodir" a fatia de 0% de progresso
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode, shadow=True)
    ax1.axis('equal')  # Garantir que o gráfico é um círculo
    st.subheader("Distribuição de Estudantes com 0% de Progresso:")
    st.pyplot(fig1)
    
    # Gráfico de Pizza 3D: Estudantes que nunca acessaram a disciplina
    fig2, ax2 = plt.subplots()
    labels = ['Nunca Acessaram', 'Já Acessaram']
    sizes = [never_accessed_count, total_students - never_accessed_count]
    explode = (0.1, 0)  # "Explodir" a fatia de nunca acessaram
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode, shadow=True)
    ax2.axis('equal')  # Garantir que o gráfico é um círculo
    st.subheader("Distribuição de Estudantes que Nunca Acessaram a Disciplina:")
    st.pyplot(fig2)
    
    # Gráfico dos últimos acessos
    # st.write("Últimos acessos por dia:")
    # st.bar_chart(last_access_count)
else:
    st.write("Nenhuma informação disponível para a disciplina selecionada.")
