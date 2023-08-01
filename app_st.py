import streamlit as st
import pandas as pd

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
            df1 = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            df1 = df.groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
        df1['Evasão'].plot(kind='bar')

    # If the user selects 2 attributes
    else:
        if values_or_percentage == 'Valores Absolutos':
            df2 = df.groupby([attribute1, attribute2])['Situação no Curso'].value_counts().unstack().fillna(0)
        else:
            df2 = df.groupby([attribute1, attribute2])['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
        df2['Evasão'].plot(kind='bar')

    # Show the plot
    st.pyplot()

