import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Disciplinas")

st.title("Base de Disciplinas")
st.write("Página para base de dados dos estudantes matriculados, docentes e tutores alocados nas disciplinas em oferta")
st.write("**Qual o relatório base?** Aqueles que não dependem dos scripts de *webscrapping* para geração das planilhas. Mais especificamente, um dos relatórios personalizados de participantes do curso")

st.sidebar.image("./icons/logoEAD.png", width=150)

# Carregar os dados do arquivo CSV
cursos = './cursosEaD/database23ago2024.csv'
data = pd.read_csv(cursos)

# Filtrar as disciplinas do Trimestre T1 e apenas os usuários com papel "Estudante"
students_data = data[data['Papel'] == 'Estudante']

# Contar o número de estudantes por disciplina
estudantes_por_disciplina = students_data.groupby('Nome completo do curso com link')['Matrícula'].count().reset_index()
estudantes_por_disciplina.columns = ['Nome completo do curso com link', 'Número de Estudantes']

# Mesclar os dados de tutores/docentes e estudantes por disciplina
tutors_and_teachers = data[data['Papel'].isin(['TutorEAD', 'DocenteEAD'])]

# Mesclagem correta com base nas disciplinas, substituindo NaN por 0
final_data = pd.merge(tutors_and_teachers, estudantes_por_disciplina, on='Nome completo do curso com link', how='left')
final_data.fillna(0, inplace=True)  # Substituir todos os NaN por 0
final_data['Número de Estudantes'] = final_data['Número de Estudantes'].astype(int)  # Converter para int

# Dividir os dados em tabelas de docentes e tutores
final_docentes_table = final_data[final_data['Papel'] == 'DocenteEAD']
final_tutores_table = final_data[final_data['Papel'] == 'TutorEAD']

# Contagem de disciplinas por tutor/docente
disciplinas_por_tutor_docente = final_data.groupby(['Nome completo com link', 'Papel'])['Nome completo do curso com link'].nunique().reset_index()
disciplinas_por_tutor_docente.columns = ['Nome completo com link', 'Papel', 'Disciplinas']

# Contagem de estudantes por tutor/docente
estudantes_por_tutor_docente = final_data.groupby(['Nome completo com link', 'Papel'])['Número de Estudantes'].sum().reset_index()

# Criação de opções para o filtro dos docentes
docente_options = ['Selecione um Docente', 'Todos os Docentes'] + list(final_docentes_table['Nome completo com link'].unique())

# Selecionar docente através de um selectbox
selected_docente = st.selectbox('Selecione um Docente:', docente_options)

# Mostrar tabela de docentes com base na seleção
if selected_docente != 'Selecione um Docente':
    if selected_docente == 'Todos os Docentes':
        # Exibir todas as disciplinas associadas a todos os docentes
        filtered_docente_table = final_docentes_table[['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes']]
    else:
        # Filtrar disciplinas associadas ao docente selecionado
        filtered_docente_table = final_docentes_table[final_docentes_table['Nome completo com link'] == selected_docente][['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes']]
    
    # Calcular total de disciplinas e estudantes
    total_disciplinas = filtered_docente_table.shape[0]
    total_estudantes = filtered_docente_table['Número de Estudantes'].sum()

    # Adicionar uma linha extra com os totais
    totals_row = pd.DataFrame([['Total', selected_docente, total_estudantes]], columns=['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes'])
    filtered_docente_table = pd.concat([filtered_docente_table, totals_row])

    # Exibir a tabela filtrada
    st.subheader(f"Tabela de Disciplinas do Docente: {selected_docente}")
    st.write(filtered_docente_table.to_html(index=False), unsafe_allow_html=True)

# Criação de opções para o filtro dos tutores
tutor_options = ['Selecione um Tutor', 'Todos os Tutores'] + list(final_tutores_table['Nome completo com link'].unique())

# Selecionar tutor através de um selectbox
selected_tutor = st.selectbox('Selecione um Tutor:', tutor_options)

# Mostrar tabela de tutores com base na seleção
if selected_tutor != 'Selecione um Tutor':
    if selected_tutor == 'Todos os Tutores':
        # Exibir todas as disciplinas associadas a todos os tutores
        filtered_tutor_table = final_tutores_table[['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes']]
    else:
        # Filtrar disciplinas associadas ao tutor selecionado
        filtered_tutor_table = final_tutores_table[final_tutores_table['Nome completo com link'] == selected_tutor][['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes']]
    
    # Calcular total de disciplinas e estudantes
    total_disciplinas = filtered_tutor_table.shape[0]
    total_estudantes = filtered_tutor_table['Número de Estudantes'].sum()

    # Adicionar uma linha extra com os totais
    totals_row = pd.DataFrame([['Total', selected_tutor, total_estudantes]], columns=['Nome completo do curso com link', 'Nome completo com link', 'Número de Estudantes'])
    filtered_tutor_table = pd.concat([filtered_tutor_table, totals_row])

    # Exibir a tabela filtrada
    st.subheader(f"Tabela de Disciplinas do Tutor: {selected_tutor}")
    st.write(filtered_tutor_table.to_html(index=False), unsafe_allow_html=True)

# Contagem de disciplinas por tutor/docente
disciplinas_por_tutor_docente = final_data.groupby(['Nome completo com link', 'Papel'])['Nome completo do curso com link'].nunique().reset_index()
disciplinas_por_tutor_docente.columns = ['Nome completo com link', 'Papel', 'Disciplinas']

# Contagem de estudantes por tutor/docente
estudantes_por_tutor_docente = final_data.groupby(['Nome completo com link', 'Papel'])['Número de Estudantes'].sum().reset_index()

# Gráfico de barras horizontal para Docentes - Quantidade de Estudantes
docentes_data = estudantes_por_tutor_docente[estudantes_por_tutor_docente['Papel'] == 'DocenteEAD']
if not docentes_data.empty:
    fig, ax = plt.subplots(figsize=(8, 16))
    ax.barh(docentes_data['Nome completo com link'], docentes_data['Número de Estudantes'], color='skyblue')
    ax.set_xlabel('Número de Estudantes')
    ax.set_ylabel('Docente')
    ax.set_title('Número de Estudantes por Docente')
    st.pyplot(fig)

# Gráfico de barras horizontal para Tutores - Quantidade de Estudantes
tutores_data = estudantes_por_tutor_docente[estudantes_por_tutor_docente['Papel'] == 'TutorEAD']
if not tutores_data.empty:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(tutores_data['Nome completo com link'], tutores_data['Número de Estudantes'], color='salmon')
    ax.set_xlabel('Número de Estudantes')
    ax.set_ylabel('Tutor')
    ax.set_title('Número de Estudantes por Tutor')
    st.pyplot(fig)

# Gráfico de Pizza para Tutores - Quantidade de Disciplinas
disciplinas_tutores_data = disciplinas_por_tutor_docente[disciplinas_por_tutor_docente['Papel'] == 'TutorEAD']
if not disciplinas_tutores_data.empty:
    fig, ax = plt.subplots(figsize=(6, 6))

    # Criar o gráfico de pizza sem labels
    wedges, _, autotexts = ax.pie(disciplinas_tutores_data['Disciplinas'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    
    # Garantir que o gráfico seja um círculo
    ax.axis('equal')

    # Adicionar uma legenda fora do gráfico associando as fatias aos tutores
    ax.legend(wedges, disciplinas_tutores_data['Nome completo com link'], title="Tutores", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Exibir o gráfico de pizza com a legenda
    st.subheader("Proporção de Disciplinas por Tutor")
    st.pyplot(fig)