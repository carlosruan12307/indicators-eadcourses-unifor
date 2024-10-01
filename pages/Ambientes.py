import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Carregar os dados do arquivo CSV
secretaria = './cursosLivres/secretaria-acessos-01out2024.csv'
data = pd.read_csv(secretaria)

# Converter a coluna 'Data' para o formato datetime
data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%y')

# Remover colunas desnecessárias
data = data.drop(['Usuário afetado', 'Componente', 'Descrição', 'Origem', 'endereço IP', 'Tipo de Ação'], axis=1)

# Título da aplicação
st.title("Outros ambientes")
st.write("Página para acompanhamento dos outros ambientes desenvolvidos pela equipe do EaD Unifor, incluindo grupos de trabalho e cursos livres.")
st.sidebar.image("./icons/logoEAD.png", width=150)

# Título da aplicação
st.header("Secretaria Virtual")

# Adicionar o filtro de data acima do gráfico
st.subheader("Filtrar por Data")

# Seletor de período com um placeholder
date_filter_option = st.selectbox(
    "Selecione o período:",
    ["Escolha o período", "Data específica", "Última semana", "Últimas duas semanas", "Último mês"]
)

# Verificar se o usuário selecionou um período válido
if date_filter_option != "Escolha o período":
    # Escolha da data caso "Data específica" seja selecionada
    if date_filter_option == "Data específica":
        selected_date = st.date_input("Escolha uma data", datetime.today())

    # Botão para gerar o relatório
    generate_report = st.button("Gerar Relatório")

    # Apenas gera o relatório se o botão for pressionado
    if generate_report:
        # Filtrar os dados com base na seleção do usuário
        if date_filter_option == "Data específica":
            filtered_data = data[data['Data'] == pd.to_datetime(selected_date)]
        elif date_filter_option == "Última semana":
            one_week_ago = datetime.today() - timedelta(weeks=1)
            filtered_data = data[data['Data'] >= one_week_ago]
        elif date_filter_option == "Últimas duas semanas":
            two_weeks_ago = datetime.today() - timedelta(weeks=2)
            filtered_data = data[data['Data'] >= two_weeks_ago]
        elif date_filter_option == "Último mês":
            one_month_ago = datetime.today() - timedelta(days=30)
            filtered_data = data[data['Data'] >= one_month_ago]

        # Calcular a quantidade total de acessos
        total_accesses = len(filtered_data)

        # Calcular a divisão de acessos por cada tipo de página
        access_counts_per_page = filtered_data['Contexto do Evento'].value_counts()

        # Calcular a quantidade total de estudantes únicos
        unique_students = filtered_data['Nome completo'].nunique()

        # Exibir os resultados
        st.subheader("Resultados do Período Selecionado")
        st.write(f"**Total de acessos:** {total_accesses}")
        st.write(f"**Quantidade total de estudantes únicos:** {unique_students}")

        st.subheader("Divisão de Acessos por Página")
        for page, count in access_counts_per_page.items():
            cleaned_page = page.replace('Página: ', '').replace('Disciplina: ', '')
            st.write(f"**{cleaned_page}**: {count} acessos")

        # Análise adicional de estudantes únicos
        students_accessing_discipline = filtered_data[filtered_data['Contexto do Evento'] == 'Disciplina: Secretaria Virtual EaD']['Nome completo'].unique()
        students_accessing_pages = filtered_data[
            filtered_data['Contexto do Evento'].str.contains('Página: ')
        ]['Nome completo'].unique()

        # Estudantes que acessaram a disciplina e também acessaram alguma página
        students_discipline_and_pages = set(students_accessing_discipline).intersection(set(students_accessing_pages))

        # Estudantes que acessaram apenas a disciplina sem acessar as páginas
        students_only_discipline = set(students_accessing_discipline).difference(students_accessing_pages)

        # Exibir os resultados da análise de estudantes únicos
        st.subheader("Análise quantitativa, qualitativa e temporal")
        st.write(f"**Total de estudantes que acessaram a disciplina (Secretaria Virtual EaD):** {len(students_accessing_discipline)}")
        st.write(f"**Total de estudantes que acessaram a disciplina e também acessaram as páginas:** {len(students_discipline_and_pages)}")
        st.write(f"**Total de estudantes que acessaram apenas a disciplina sem entrar nas páginas:** {len(students_only_discipline)}")

        # Dados para o gráfico de pizza
        labels = [
            'Disciplina e Páginas',
            'Apenas a Disciplina'
        ]
        sizes = [len(students_discipline_and_pages), len(students_only_discipline)]
        colors = ['#66b3ff', '#99ff99']
        explode = (0.1, 0)  # Destaque para o primeiro segmento

        # Criar o gráfico de pizza
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equaliza o gráfico de pizza

        # Exibir o gráfico de pizza no Streamlit
        st.pyplot(fig)

        # Gráfico de linha para análise temporal dos acessos
        # st.subheader("Análise Temporal dos Acessos")

        # Agrupar os acessos por data
        accesses_by_date = filtered_data.groupby(filtered_data['Data'].dt.date).size()

        # Certifique-se de que o índice está como datetime
        accesses_by_date.index = pd.to_datetime(accesses_by_date.index)

        # Criar o gráfico de linha
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(accesses_by_date.index, accesses_by_date.values, marker='o', linestyle='-', color='b', label="Acessos")

        ax.set_xlabel('Data')
        ax.set_ylabel('Número de Acessos')
        ax.set_title('Evolução dos Acessos ao Longo do Tempo')

        # Adicionar linhas pontilhadas verticais para cada ponto de data no eixo x
        for date in accesses_by_date.index:
            ax.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

        # Ajustar os rótulos das datas para maior legibilidade
        ax.set_xticks(accesses_by_date.index)
        ax.set_xticklabels(accesses_by_date.index.strftime('%d/%m/%Y'), rotation=45, ha="right")

        # Ajustar o espaçamento para que os rótulos não se sobreponham
        plt.tight_layout()

        # Adicionar legenda
        ax.legend()

        # Exibir o gráfico de linha no Streamlit
        st.pyplot(fig)
else:
    st.info("Por favor, selecione um período para gerar o relatório.")
