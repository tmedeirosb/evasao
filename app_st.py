import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("Relatorio-dados-2.csv")

# Add a selectbox for the user to choose the modalidade
modalidade = st.sidebar.selectbox('Selecione a modalidade:', df['Modalidade'].unique())

# Filter the data based on the selected modalidade
df = df[df['Modalidade'] == modalidade]

# Add a selectbox for the user to choose between absolute values and percentage
values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

# Add selectboxes for the user to choose one or two attributes
attribute1 = st.sidebar.selectbox('Selecione o primeiro atributo:', df.columns)
attribute2 = st.sidebar.selectbox('Selecione o segundo atributo (opcional):', df.columns.insert(0, 'Nenhum'))

# Add a "Visualizar" button
visualizar = st.sidebar.button('Visualizar')

# If the "Visualizar" button is pressed
if visualizar:
    # If the user selects only 1 attribute
    if attribute2 == 'Nenhum':
        if values_or_percentage == 'Valores Absolutos':
            data_to_plot = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            data_to_plot = df.groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
        data_to_plot['Evasão'].plot(kind='bar')
        plt.title('Evasão por ' + attribute1)
        plt.xlabel(attribute1)
        plt.ylabel('Evasão')

    # If the user selects 2 attributes
    else:
        plt.figure(figsize=(15, 10))
        if values_or_percentage == 'Valores Absolutos':
            sns.countplot(data=df, x=attribute1, hue=attribute2)
        else:
            df_grouped = df.groupby([attribute1, attribute2]).size().unstack(fill_value=0)
            df_grouped = df_grouped.divide(df_grouped.sum(axis=1), axis=0)
            df_grouped.plot(kind='bar', stacked=True)
        plt.title('Evasão por ' + attribute1 + ' e ' + attribute2)
        plt.xlabel(attribute1)
        plt.ylabel('Evasão')

    # Show the plot
    st.pyplot()


