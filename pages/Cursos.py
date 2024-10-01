import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.image("./icons/logoEAD.png", width=150)

# Definir as cores e sombra como variáveis
shadow_opacity = 0  # Nível de opacidade da sombra (0 a 1, onde 1 é totalmente opaco)
colors_progress = ['#ff9999', '#66b3ff']  # Cores para o gráfico de progresso
colors_access = ['#99ff99', '#ffcc99']   # Cores para o gráfico de acesso
legend_fontsize = 8

# Carregar os dados do arquivo CSV
cursos = './cursosEaD/database23ago2024.csv'
data = pd.read_csv(cursos)

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
    never_accessed_count = course_data[course_data['Último acesso a disciplina'].isna() | (course_data['Último acesso a disciplina'] == "Nunca")].shape[0]
    
    last_access_count = course_data['Último acesso a disciplina'].value_counts()
    
    return total_students, progress_mean, zero_progress_count, never_accessed_count, last_access_count

# Gerar métricas para a disciplina selecionada
if not course_data.empty:
    total_students, progress_mean, zero_progress_count, never_accessed_count, last_access_count = generate_metrics(course_data)
    
    # Exibir as informações estilizadas usando HTML e CSS
    st.markdown(f"""
        <style>
            .metric-box {{
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, {shadow_opacity});
                background-color: #f9f9f9;
            }}
            .metric-box h2 {{
                margin: 0;
                font-size: 20px;
                color: #333;
            }}
            .metric-box p {{
                margin: 0;
                font-size: 16px;
                color: #555;
            }}
        </style>
        
        <div class="metric-box">
            <h2>Disciplina: {selected_course}</h2>
            <p>Total de estudantes: {total_students}</p>
            <p>Média do progresso: {progress_mean:.2f}%</p>
            <p>Estudantes com 0% de progresso: {zero_progress_count}</p>
            <p>Estudantes que nunca acessaram: {never_accessed_count}</p>
        </div>
    """, unsafe_allow_html=True)

    # Gráfico de Pizza 3D: Estudantes com 0% de progresso
    fig1, ax1 = plt.subplots(figsize=(5, 4))  # Define a largura (5) e a altura (4) da figura
    labels = ['0% de Progresso', 'Outros']
    sizes = [zero_progress_count, total_students - zero_progress_count]
    explode = (0.1, 0)  # "Explodir" a fatia de 0% de progresso
    wedges, texts, autotexts = ax1.pie(
        sizes, autopct='%1.1f%%', startangle=90, explode=explode, 
        colors=colors_progress, textprops={'fontsize': 8},
        wedgeprops=dict(linewidth=1)
    )
    ax1.axis('equal')  # Garantir que o gráfico é um círculo
    
    # Adicionar a legenda
    ax1.legend(wedges, labels, title="Progresso", loc="lower right", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=legend_fontsize)

    st.pyplot(fig1)
    
    # Gráfico de Pizza 3D: Estudantes que nunca acessaram a disciplina
    fig2, ax2 = plt.subplots(figsize=(5, 4))  # Define a largura (5) e a altura (4) da figura
    labels = ['Nunca Acessaram', 'Já Acessaram']
    sizes = [never_accessed_count, total_students - never_accessed_count]
    wedges, texts, autotexts = ax2.pie(
        sizes, autopct='%1.1f%%', startangle=90, explode=explode, 
        colors=colors_access, textprops={'fontsize': 8},
        wedgeprops=dict(linewidth=1)
    )
    ax2.axis('equal')  # Garantir que o gráfico é um círculo
    
    # Adicionar a legenda
    ax2.legend(wedges, labels, title="Acesso", loc="lower right", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=legend_fontsize)

    st.pyplot(fig2)
else:
    st.write("Nenhuma informação disponível para a disciplina selecionada.")
