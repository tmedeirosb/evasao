
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache
def load_data():
    df = pd.read_csv("Relatorio-dados-st.csv")
    df_tec_integrado = df[df['Modalidade'] == 'Técnico Integrado']
    df_tec_integrado['Status'] = df_tec_integrado['Situação no Curso'].apply(lambda x: 'Evasão' if x == 'Evasão' else 'Outro status')
    return df_tec_integrado

df = load_data()

# Select the attribute(s)
attribute1 = st.selectbox('Select the first attribute:', df.columns)
attribute2 = st.selectbox('Select the second attribute (optional):', [''] + list(df.columns))

# Select the display option
display_option = st.selectbox('Select the display option:', ['Percentage', 'Absolute Value'])

# Display the evasion rate or the interaction between the selected attributes and evasion
if attribute2:
    st.header(f'Interaction between {attribute1} and {attribute2} and Evasion')
    if display_option == 'Percentage':
        evasao_counts = df[df['Status'] == 'Evasão'].groupby([attribute1, attribute2]).size()
        total_counts = df.groupby([attribute1, attribute2]).size()
        evasao_rate = (evasao_counts / total_counts) * 100
        evasao_rate_df = evasao_rate.reset_index()
        evasao_rate_df.columns = [attribute1, attribute2, 'Evasion Rate (%)']
        plt.figure(figsize=(10, 6))
        sns.catplot(x=attribute1, y='Evasion Rate (%)', hue=attribute2, data=evasao_rate_df, kind="bar", palette="muted")
        plt.xticks(rotation='vertical')
    else:
        evasao_counts = df[df['Status'] == 'Evasão'].groupby([attribute1, attribute2]).size()
        evasao_counts_df = evasao_counts.reset_index()
        evasao_counts_df.columns = [attribute1, attribute2, 'Evasion Count']
        plt.figure(figsize=(10, 6))
        sns.catplot(x=attribute1, y='Evasion Count', hue=attribute2, data=evasao_counts_df, kind="bar", palette="muted")
        plt.xticks(rotation='vertical')
else:
    if display_option == 'Percentage':
        st.header(f'Evasion Rate for {attribute1}')
        evasao_counts = df[df['Status'] == 'Evasão'].groupby(attribute1).size()
        total_counts = df.groupby(attribute1).size()
        evasao_rate = (evasao_counts / total_counts) * 100
        plt.figure(figsize=(10, 6))
        sns.barplot(x=evasao_rate.index, y=evasao_rate.values, color='blue')
    else:
        st.header(f'Evasion Count for {attribute1}')
        evasao_counts = df[df['Status'] == 'Evasão'].groupby(attribute1).size()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=evasao_counts.index, y=evasao_counts.values, color='blue')
st.pyplot(plt.gcf())
