
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

# Tab selection
tab_selection = st.sidebar.radio("Selecione a aba", ['Aba 1', 'Aba 2'])

# Common sidebar components
modalidade = st.sidebar.selectbox('Selecione a modalidade:', ['Nenhum'] + list(df['Modalidade'].unique()))
tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', ['Nenhum'] + list(df['Tipo de Escola de Origem'].unique()))
situacoes_to_display = st.sidebar.multiselect('Selecione as situações a serem exibidas:', list(df['Situação no Curso'].unique()))

# Apply filters based on the selected options (skip if "Nenhum" is selected)
if modalidade != 'Nenhum':
    df = df[df['Modalidade'] == modalidade]
if tipo_escola_origem != 'Nenhum':
    df = df[df['Tipo de Escola de Origem'] == tipo_escola_origem]

values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])
visualizar = st.sidebar.button('Visualizar')

if tab_selection == 'Aba 1':
    attribute1 = st.sidebar.selectbox('Selecione o atributo:', attributes_options)

    # Logic for visualization in Aba 1
    if visualizar:
        fig, ax = plt.subplots(figsize=(15, 10))
        
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
            data_to_plot.plot(kind='bar', ax=ax)
            ax.set_ylabel('Quantidade')
        else:
            data_to_plot_percentage = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0) * 100
            data_to_plot_percentage.plot(kind='bar', ax=ax)
            ax.set_ylabel('Porcentagem (%)')

        ax.set_title('Situação no Curso por ' + attribute1)
        ax.set_xlabel(attribute1)
        for container in ax.containers:
            ax.bar_label(container)

        # Show the plot
        st.pyplot(fig)
        
        # Display data table
        data_to_plot['Total'] = data_to_plot.sum(axis=1)
        data_to_plot.loc['Total'] = data_to_plot.sum()
        st.write(data_to_plot)

elif tab_selection == 'Aba 2':
    attribute1 = st.sidebar.selectbox('Selecione o primeiro atributo:', attributes_options)
    attribute2 = st.sidebar.selectbox('Selecione o segundo atributo (opcional):', ['Nenhum'] + attributes_options)

    # Logic for visualization in Aba 2
    if visualizar:
        fig, ax = plt.subplots(figsize=(15, 10))
        
        if attribute2 == 'Nenhum':
            data_to_plot = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
            if values_or_percentage == 'Valores Absolutos':
                data_to_plot.plot(kind='bar', ax=ax)
                ax.set_ylabel('Quantidade')
            else:
                data_to_plot_percentage = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0) * 100
                data_to_plot_percentage.plot(kind='bar', ax=ax)
                ax.set_ylabel('Porcentagem (%)')
            
            ax.set_title('Situação no Curso por ' + attribute1)
            ax.set_xlabel(attribute1)
            for container in ax.containers:
                ax.bar_label(container)

        else:
            if values_or_percentage == 'Valores Absolutos':
                sns.countplot(data=df[df['Situação no Curso'].isin(situacoes_to_display)], x=attribute1, hue=attribute2, ax=ax)
            else:
                # Complex normalization logic for percentage visualization
                df_grouped = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby([attribute1, attribute2]).size().unstack(fill_value=0)
                total_by_group = df[df['Situação no Curso'].isin(situacoes_to_display)].groupby(attribute1).size()
                df_grouped_percentage = (df_grouped.divide(total_by_group, axis=0) * 100).fillna(0)
                df_grouped_percentage.plot(kind='bar', ax=ax)
                ax.set_ylabel('Porcentagem (%)')
            
            ax.set_title('Situação no Curso por ' + attribute1 + ' e ' + attribute2)
            ax.set_xlabel(attribute1)
            for container in ax.containers:
                ax.bar_label(container)

        # Show the plot
        st.pyplot(fig)
        
        # Display data table
        data_to_plot['Total'] = data_to_plot.sum(axis=1)
        data_to_plot.loc['Total'] = data_to_plot.sum()
        st.write(data_to_plot)
