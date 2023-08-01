
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv("Relatorio-dados-2.csv")

# Define the options for the attribute selection
attributes_options = ['Código Curso', 'Campus', 'Descrição do Curso', 'Ano Letivo de Previsão de Conclusão', 'Ano de Ingresso', 'Período Atual', 'Modalidade']

# Add 'Nenhum' to the options
attribute_options_with_none = ['Nenhum'] + attributes_options

# Add a selectbox for the user to choose the modalidade
modalidade = st.sidebar.selectbox('Selecione a modalidade:', df['Modalidade'].unique())

# Filter the data based on the selected modalidade
df = df[df['Modalidade'] == modalidade]

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
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            data_to_plot = df.groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
        data_to_plot['Evasão'].plot(kind='bar', ax=ax)
        ax.set_title('Evasão por ' + attribute1)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Evasão')
        for container in ax.containers:
            ax.bar_label(container)
        # Add a horizontal line for the mean
        ax.axhline(y=data_to_plot['Evasão'].mean(), color='r', linestyle='--')

    # If the user selects 2 attributes
    else:
        if values_or_percentage == 'Valores Absolutos':
            plot = sns.countplot(data=df, x=attribute1, hue=attribute2, ax=ax)
        else:
            df_grouped = df.groupby([attribute1, attribute2]).size().unstack(fill_value=0)
            df_grouped = df_grouped.divide(df_grouped.sum(axis=1), axis=0)
            df_grouped.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title('Evasão por ' + attribute1 + ' e ' + attribute2)
        ax.set_xlabel(attribute1)
        ax.set_ylabel('Evasão')
        for container in ax.containers:
            ax.bar_label(container)
        # Add a horizontal line for the mean
        ax.axhline(y=df_grouped.mean().mean(), color='r', linestyle='--')

    # Show the plot
    st.pyplot(fig)


