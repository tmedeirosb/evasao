
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

    # Sidebar
    with st.sidebar:
        st.header("Visualização")

        # Situação do curso
        situation = st.selectbox('Selecione a situação do curso:', df['Situação no Curso'].unique())

        # Valores absolutos ou porcentagem
        values_or_percentage = st.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

        st.header("Interação variáveis")

        # Seleção de atributos para interação
        attribute1 = st.selectbox('Seleção do atributo 1:', attributes_options)
        attribute_values_1 = st.multiselect(f'Valores para {attribute1}:', df[attribute1].unique())

        attribute2 = st.selectbox('Seleção do atributo 2:', attributes_options)
        if attribute_values_1:
            df_filtered_by_attr1 = df[df[attribute1].isin(attribute_values_1)]
            attribute_values_2 = st.multiselect(f'Valores para {attribute2} (baseado em {attribute1}):', df_filtered_by_attr1[attribute2].unique())
        else:
            attribute_values_2 = []

        # Botão para visualizar
        visualize_button = st.button('Visualizar')

    # Main content
    if visualize_button:
        # Filtering data based on selected attributes
        df_filtered = df[df[attribute1].isin(attribute_values_1) & df[attribute2].isin(attribute_values_2)]

        # Plot
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.countplot(data=df_filtered, x=attribute2, hue=situation, ax=ax)
        ax.set_title(f"{situation} por {attribute2}")
        for container in ax.containers:
            ax.bar_label(container)
        st.pyplot(fig)

        # Display table
        table_data = df_filtered.groupby([attribute2])[situation].value_counts().unstack().fillna(0)
        table_data['Total'] = table_data.sum(axis=1)
        table_data.loc['Total'] = table_data.sum()
        st.write(table_data)

    # Adjusting the sidebar scroll
    st.markdown("""
        <style>
            .sidebar .sidebar-content {
                height: auto !important;
                overflow: auto;
                width: 330px;
                position: fixed;
            }
        </style>
        """, unsafe_allow_html=True)
