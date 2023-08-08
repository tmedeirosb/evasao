
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

if tab == "Interação entre variáveis":
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
        if situation and attribute_values_1 and attribute_values_2:
            df_filtered = df[df['Situação no Curso'] == situation]
            fig, ax = plt.subplots(figsize=(15, 10))
            data = df_filtered[df_filtered[attribute1].isin(attribute_values_1) & df_filtered[attribute2].isin(attribute_values_2)]
            grouped_data = data.groupby(attribute2).size()
            
            if values_or_percentage == 'Valores Absolutos':
                data_to_plot = grouped_data
            else:
                total = len(df_filtered)
                data_to_plot = (grouped_data / total * 100).fillna(0)
                
            data_to_plot.plot(kind='bar', ax=ax)
            ax.set_title(f'Situação {situation} por {attribute2} (baseado em {attribute1})')
            ax.set_xlabel(attribute2)
            ax.set_ylabel('Count' if values_or_percentage == 'Valores Absolutos' else 'Percentage (%)')
            for container in ax.containers:
                ax.bar_label(container)
            st.pyplot(fig)
            
            # Exibindo a tabela
            grouped_data_df = pd.DataFrame(grouped_data)
            grouped_data_df['Total'] = grouped_data_df.sum(axis=1)
            grouped_data_df.loc['Total'] = grouped_data_df.sum()
            st.write(grouped_data_df)
        else:
            st.warning("Por favor, selecione uma situação do curso e valores para os atributos.")
    
    st.write("\n \n \n \n ")
