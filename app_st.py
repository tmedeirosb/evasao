
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

# Add selectboxes for the user to choose one or two attributes
attribute1 = st.sidebar.selectbox('Selecione o primeiro atributo:', attributes_options)
attribute2 = st.sidebar.selectbox('Selecione o segundo atributo (opcional):', ['Nenhum'] + attributes_options)

# Add a "Visualizar" button
visualizar = st.sidebar.button('Visualizar')

# Create a variable to store the data for the table
table_data = None

# If the "Visualizar" button is pressed
if visualizar:
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Adjust data visualization based on the selected "Situações no Curso"
    if situacoes_to_display:
        display_df = df[df['Situação no Curso'].isin(situacoes_to_display)]
    else:
        display_df = df.copy()

    # If the user selects only 1 attribute
    if attribute2 == 'Nenhum':
        grouped_data = display_df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = grouped_data.sum(axis=1)
        else:
            total_by_group = grouped_data.sum(axis=1)
            data_to_plot = grouped_data.divide(total_by_group, axis=0).sum(axis=1) * 100
        
        data_to_plot.plot(kind='bar', ax=ax, label='Dados')
        
        ax.set_title('Situação no Curso por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Quantidade')
        for container in ax.containers:
            ax.bar_label(container)
        
        # Add a horizontal line for the mean
        ax.axhline(y=data_to_plot.mean(), color='r', linestyle='--')

        # Store the data for the table
        table_data = grouped_data

    # If the user selects 2 attributes
    else:
        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=display_df, x=attribute1, hue=attribute2, ax=ax)
            table_data = display_df.groupby([attribute1, attribute2]).size().unstack(fill_value=0)
        else:
            df_grouped = display_df.groupby([attribute1, attribute2]).size().unstack(fill_value=0)
            total_by_group = display_df.groupby(attribute1).size()
            df_grouped = df_grouped.divide(total_by_group, axis=0) * 100
            df_grouped.plot(kind='bar', stacked=False, ax=ax)
            table_data = df_grouped

        ax.set_title('Situação no Curso por ' + attribute1 + ' e ' + attribute2)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Percentual')
        for container in ax.containers:
            ax.bar_label(container)

        # Add a horizontal line for the mean
        ax.axhline(y=df_grouped.mean().mean(), color='r', linestyle='--')

    # Show the plot
    st.pyplot(fig)

    # Display the table data
    if table_data is not None:
        table_data['Total'] = table_data.sum(axis=1)
        table_data.loc['Total'] = table_data.sum()
        st.write(table_data)
