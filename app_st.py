
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
attributes_options = ['Código Curso', 'Campus', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 'Período Atual', 'Modalidade', 'Status']

# Add 'Nenhum' to the options
attribute_options_with_none = ['Nenhum'] + attributes_options

# Add selectboxes for the user to choose filters (with "Nenhum" option)
modalidade = st.sidebar.selectbox('Selecione a modalidade:', ['Nenhum'] + list(df['Modalidade'].unique()))
tipo_escola_origem = st.sidebar.selectbox('Selecione o tipo de escola de origem:', ['Nenhum'] + list(df['Tipo de Escola de Origem'].unique()))
status = st.sidebar.selectbox('Selecione o status:', ['Nenhum'] + list(df['Status'].unique()))

# Apply filters based on the selected options (skip if "Nenhum" is selected)
if modalidade != 'Nenhum':
    df = df[df['Modalidade'] == modalidade]
if tipo_escola_origem != 'Nenhum':
    df = df[df['Tipo de Escola de Origem'] == tipo_escola_origem]
if status != 'Nenhum':
    df = df[df['Status'] == status]

# Add a selectbox for the user to choose between absolute values and percentage
values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

# Add selectboxes for the user to choose one or two attributes
attribute1 = st.sidebar.selectbox('Selecione o primeiro atributo:', attributes_options)
attribute2 = st.sidebar.selectbox('Selecione o segundo atributo (opcional):', attribute_options_with_none)

# Add a "Visualizar" button
visualizar = st.sidebar.button('Visualizar')

# If the "Visualizar" button is pressed
if visualizar:
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # If the user selects only 1 attribute
    if attribute2 == 'Nenhum':
        total_values = df[attribute1].value_counts().sum()
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = df[attribute1].value_counts().sort_index()
        else:
            data_to_plot = (df[attribute1].value_counts() / total_values * 100).sort_index()
        
        data_to_plot.plot(kind='bar', ax=ax, label='Dados')
        
        # Add a bar for the total values
        if values_or_percentage == 'Valores Absolutos':
            ax.bar('Total', total_values, color='grey', label='Total')
        
        ax.set_title('Status por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Status')
        for container in ax.containers:
            ax.bar_label(container)
        
        # Add a horizontal line for the mean
        ax.axhline(y=data_to_plot.mean(), color='r', linestyle='--')

    # If the user selects 2 attributes
    else:
        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=df, x=attribute1, hue=attribute2, ax=ax)
        else:
            df_grouped = df.groupby([attribute1, attribute2]).size().unstack(fill_value=0)
            total_by_group = df.groupby(attribute1).size()
            df_grouped = df_grouped.divide(total_by_group, axis=0) * 100
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
