
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

# Load the data
df = pd.read_csv("Relatorio-dados-2.csv")

# Define a function to categorize status
def categorize_status(row):
    today_year = datetime.datetime.now().year

    if row['Situação no Curso'] == 'Evasão':
        return 'Evasão'
    elif row['Situação no Curso'] in ['Matriculado', 'Matricula Vinculo']:
        if row['Ano Letivo de Previsão de Conclusão'] > today_year:
            return 'Retenção'
        else:
            return 'Regular'
    else:
        return 'Outro'

# Apply the function to create the new 'Status' column
df['Status'] = df.apply(categorize_status, axis=1)

# Define the options for the attribute selection
attributes_options = ['Código Curso', 'Campus', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 'Período Atual', 'Modalidade']

# Add 'Nenhum' to the options for filters
filter_options_with_none = ['Nenhum'] + list(df['Modalidade'].unique()) + list(df['Tipo de Escola de Origem'].unique()) + list(df['Status'].unique())

# Add selectboxes for the user to choose filters (with "Nenhum" option)
modalidade = st.sidebar.selectbox('Selecione a modalidade:', filter_options_with_none)
tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', filter_options_with_none)
status_to_display = st.sidebar.selectbox('Selecione o status a ser exibido:', filter_options_with_none)

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

# If the "Visualizar" button is pressed
if visualizar:
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # If the user selects only 1 attribute
    if attribute2 == 'Nenhum':
        grouped_data = df.groupby(attribute1)['Status'].value_counts().unstack().fillna(0)
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = grouped_data[status_to_display]
        else:
            total_by_group = grouped_data.sum(axis=1)
            data_to_plot = (grouped_data[status_to_display] / total_by_group * 100).fillna(0)
        
        data_to_plot.plot(kind='bar', ax=ax, label='Dados')
        
        ax.set_title('Status por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Status (%)')
        for container in ax.containers:
            ax.bar_label(container)
        
        # Add a horizontal line for the mean
        ax.axhline(y=data_to_plot.mean(), color='r', linestyle='--')

    # If the user selects 2 attributes
    else:
        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=df[df['Status'] == status_to_display], x=attribute1, hue=attribute2, ax=ax)
        else:
            df_grouped = df[df['Status'] == status_to_display].groupby([attribute1, attribute2]).size().unstack(fill_value=0)
            total_by_group = df.groupby(attribute1).size()
            df_grouped = (df_grouped.divide(total_by_group, axis=0) * 100).fillna(0)
            df_grouped.plot(kind='bar', stacked=True, ax=ax)
        
        ax.set_title('Status por ' + attribute1 + ' e ' + attribute2)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Status (%)')
        for container in ax.containers:
            ax.bar_label(container)
        
        # Add a horizontal line for the mean
        ax.axhline(y=df_grouped.mean().mean(), color='r', linestyle='--')

    # Show the plot
    st.pyplot(fig)
