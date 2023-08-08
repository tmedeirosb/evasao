
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

    with st.sidebar.container():
        st.sidebar.header("Visualização")

        # Situação do curso
        situation = st.sidebar.selectbox('Selecione a situação do curso:', df['Situação no Curso'].unique())

        # Valores absolutos ou porcentagem
        values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

        st.sidebar.header("Interação variáveis")

        # Seleção de atributos para interação
        attribute1 = st.sidebar.selectbox('Seleção do atributo 1:', attributes_options)
        attribute_values_1 = st.sidebar.multiselect(f'Valores para {attribute1}:', df[attribute1].unique())

        attribute2 = st.sidebar.selectbox('Seleção do atributo 2:', attributes_options)
        if attribute_values_1:
            df_filtered_by_attr1 = df[df[attribute1].isin(attribute_values_1)]
            attribute_values_2 = st.sidebar.multiselect(f'Valores para {attribute2} (baseado em {attribute1}):', df_filtered_by_attr1[attribute2].unique())
        else:
            attribute_values_2 = []

        # Botão para visualizar
        if st.sidebar.button('Visualizar'):
            pass  # Restante do código...

    # Adicionando estilização para ter uma barra de rolagem no sidebar
    st.markdown("""
        <style>
            .reportview-container .main .block-container {
                max-width: 100%;
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
                padding-bottom: 1rem;
            }
            div.stButton > button:first-child {
                width: 100%;
            }
            .sidebar .sidebar-content {
                height: auto !important;
                overflow: auto;
                width: 330px;
                position: fixed;
            }
        </style>
        """, unsafe_allow_html=True)
