
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Load the data
df = pd.read_csv("Relatorio-dados-2.csv")

# Remove all values from "Tipo de Escola de Origem" that are not "Pública" or "Privada"
df = df[df['Tipo de Escola de Origem'].isin(['Pública', 'Privada'])]

# Define the options for the attribute selection
attributes_options = ['Código Curso', 'Campus', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Tipo de Escola de Origem']

# Tabs
tabs = ["Agregação por Situação no Curso", "Interação entre variáveis"]
selected_tab = st.sidebar.radio("Escolha uma aba:", tabs)

if selected_tab == "Agregação por Situação no Curso":

    # Add multiselect for the user to choose filters (with "Nenhum" option)
    modalidade = st.sidebar.selectbox('Selecione a modalidade:', ['Nenhum'] + list(df['Modalidade'].unique()))
    tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', ['Nenhum'] + list(df['Tipo de Escola de Origem'].unique()))
    situacoes_to_display = st.sidebar.multiselect('Selecione as situações a serem exibidas:', list(df['Situação no Curso'].unique()))

    # Apply filters based on the selected options (skip if "Nenhum" is selected)
    if modalidade != 'Nenhum':
        df = df[df['Modalidade'] == modalidade]
    if tipo_escola_origem != 'Nenhum':
        df = df[df['Tipo de Escola de Origem'] == tipo_escola_origem]

    # Add a selectbox for the user to choose between absolute values and percentage
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

    # Add selectbox for the user to choose one attribute
    attribute1 = st.sidebar.selectbox('Selecione o atributo:', attributes_options)

    # Add a "Visualizar" button
    visualizar = st.sidebar.button('Visualizar')

    # Variable to store table data
    table_data = None

    # If the "Visualizar" button is pressed
    if visualizar:
        fig, ax = plt.subplots(figsize=(15, 10))

        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=df, x=attribute1, hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax)
            table_data = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            # For percentage, we need to adjust the data
            total_counts = df[attribute1].value_counts()
            status_counts = df.groupby(attribute1)['Situação no Curso'].value_counts()
            status_percentage = status_counts.div(total_counts, level=0) * 100
            status_percentage = status_percentage.reset_index(name='Percentage')
            plot = sns.barplot(data=status_percentage, x=attribute1, y='Percentage', hue='Situação no Curso', order=df[attribute1].value_counts().index, hue_order=situacoes_to_display, ax=ax)
            table_data = status_percentage.pivot(index=attribute1, columns='Situação no Curso', values='Percentage')

        ax.set_title('Situação no Curso por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Quantidade' if values_or_percentage == 'Valores Absolutos' else 'Percentual (%)')
        ax.legend(title='Situação no Curso')

        # Display the values on top of each bar
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        # Show the plot
        st.pyplot(fig)

        # Add totals to the table data
        if table_data is not None:
            table_data['Total'] = table_data.sum(axis=1)
            table_data.loc['Total'] = table_data.sum()
            st.write(table_data)

elif selected_tab == "Interação entre variáveis":
    st.sidebar.header("Filtrar base")
    filters = {attribute: st.sidebar.selectbox(f'Selecione {attribute}:', ['Nenhum'] + list(df[attribute].unique())) for attribute in attributes_options}
    df_filtered = df.copy()
    for attribute, value in filters.items():
        if value != 'Nenhum':
            df_filtered = df_filtered[df_filtered[attribute] == value]
    
    st.sidebar.header("Visualização")
    # Situação do curso
    situations = st.sidebar.multiselect('Selecione as situações do curso:', df_filtered['Situação no Curso'].unique())

    # Valores absolutos ou porcentagem
    values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])
    
    st.sidebar.header("Interação variáveis")
    # Seleção de atributos para interação
    attribute1 = st.sidebar.selectbox('Seleção do atributo 1:', attributes_options)
    attribute_values_1 = st.sidebar.multiselect(f'Valores para {attribute1}:', df_filtered[attribute1].unique())
    
    attribute2 = st.sidebar.selectbox('Seleção do atributo 2:', attributes_options)
    if attribute_values_1:
        df_filtered_by_attr1 = df_filtered[df_filtered[attribute1].isin(attribute_values_1)]
        attribute_values_2 = st.sidebar.multiselect(f'Valores para {attribute2} (baseado em {attribute1}):', df_filtered_by_attr1[attribute2].unique())
    else:
        attribute_values_2 = []

    # Botão para visualizar
    if st.sidebar.button('Visualizar'):
        if situations and attribute_values_1 and attribute_values_2:
            df_filtered = df_filtered[df_filtered['Situação no Curso'].isin(situations)]
            fig, ax = plt.subplots(figsize=(15, 10))
            data = df_filtered[df_filtered[attribute1].isin(attribute_values_1) & df_filtered[attribute2].isin(attribute_values_2)]
            grouped_data = data.groupby(attribute2)['Situação no Curso'].value_counts().unstack().fillna(0)
            if values_or_percentage == 'Valores Absolutos':
                data_to_plot = grouped_data
            else:
                total_by_group = grouped_data.sum(axis=1)
                data_to_plot = (grouped_data.T / total_by_group * 100).T.fillna(0)
            data_to_plot.plot(kind='bar', ax=ax)
            ax.set_title(f'Situação no Curso por {attribute2} (baseado em {attribute1})')
            ax.set_xlabel(attribute2)
            ax.set_ylabel('Count' if values_or_percentage == 'Valores Absolutos' else 'Percentage (%)')
            for container in ax.containers:
                ax.bar_label(container)
            st.pyplot(fig)
            # Exibindo a tabela
            grouped_data['Total'] = grouped_data.sum(axis=1)
            grouped_data.loc['Total'] = grouped_data.sum()
            st.write(grouped_data)
        else:
            st.warning("Por favor, selecione ao menos uma situação do curso e valores para os atributos.")
