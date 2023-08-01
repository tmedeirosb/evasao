import streamlit as st
import pandas as pd

# Load the data
xls = pd.ExcelFile('Relatorio-dados-2.xls')
sheet_names = xls.sheet_names
df = xls.parse(sheet_names[0])

# Add a selectbox for the user to choose the modalidade
modalidade = st.sidebar.selectbox('Selecione a modalidade:', df['Modalidade'].unique())

# Filter the data based on the selected modalidade
df = df[df['Modalidade'] == modalidade]

# Add a selectbox for the user to choose between absolute values and percentage
values_or_percentage = st.sidebar.selectbox('Selecione a forma de exibição:', ['Valores Absolutos', 'Porcentagem'])

# Add a selectbox for the user to choose one or two attributes
option = st.sidebar.selectbox('Selecione o número de atributos:', ['1', '2'])

# If the user selects 1
if option == '1':
    attribute1 = st.sidebar.selectbox('Selecione o atributo:', df.columns)
    if values_or_percentage == 'Valores Absolutos':
        df1 = df.groupby(attribute1)['Situação no Curso'].value_counts().unstack().fillna(0)
    else:
        df1 = df.groupby(attribute1)['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
    df1['Evasão'].plot(kind='bar')

# If the user selects 2
else:
    attribute1 = st.sidebar.selectbox('Selecione o primeiro atributo:', df.columns)
    attribute2 = st.sidebar.selectbox('Selecione o segundo atributo:', df.columns)
    if values_or_percentage == 'Valores Absolutos':
        df2 = df.groupby([attribute1, attribute2])['Situação no Curso'].value_counts().unstack().fillna(0)
    else:
        df2 = df.groupby([attribute1, attribute2])['Situação no Curso'].value_counts(normalize=True).unstack().fillna(0)
    df2['Evasão'].plot(kind='bar')

# Show the plot
st.pyplot()
