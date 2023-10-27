import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Carregar dados
df_inc = pd.read_csv("fires.csv", sep=';')
df_ind = pd.read_csv("dataset_indigenas.csv", sep=';', encoding='latin-1', decimal=',')

# Extrair o ano da coluna 'date' e criar uma nova coluna 'year'
df_inc['year'] = df_inc['date'].apply(lambda x: int(x.split('/')[0]))

# Renomear colunas
df_inc.rename(columns={'class': 'Classe'}, inplace=True)


# Sidebar
st.sidebar.header("Filtros")
ano_selected = st.sidebar.selectbox("Selecione o ano", df_ind["ANO"].unique())
classe_selected = st.sidebar.multiselect("Selecione as classes de desmatamento", df_inc["Classe"].unique())
estado_selected = st.sidebar.multiselect("Selecione os estados", df_inc["uf"].unique())

# Filtros baseados na seleção da sidebar
df_inc_filtered = df_inc[df_inc["Classe"].isin(classe_selected) & df_inc["uf"].isin(estado_selected)]
df_ind_selected = df_ind[df_ind["ANO"] == ano_selected]

# Criação de gráficos
st.title("Análise de Desmatamento")

# Gráfico de desmatamento por classe
if classe_selected:
    st.subheader("Tipos de Desmatamentos")
    fig = px.pie(df_inc_filtered, names='Classe', title='Distribuição dos tipos de desmatamento')
    st.plotly_chart(fig)

# Gráfico de desmatamento por estado
if estado_selected:
    st.subheader("Distribuição de Desmatamentos por Estados")
    fig = px.pie(df_inc_filtered, names='uf', title='Distribuição dos desmatamentos por estado')
    st.plotly_chart(fig)

# Gráfico de área desmatada por ano
st.subheader(f"Área desmatada em {ano_selected}")
fig = px.bar(df_ind_selected, x='TRIBO', y='AREA', title=f'Área desmatada por tribo em {ano_selected}')
st.plotly_chart(fig)

# Comparação entre quantidade de desmatamentos e área perdida
st.subheader("Comparação entre quantidade de desmatamentos e área perdida")
# Lista de anos
anos = df_ind["ANO"].unique()

# Cálculo de valores agregados para cada ano
quantidade_desmatamentos = [df_inc[df_inc["year"] == ano].shape[0] for ano in anos]
area_perdida = [df_ind[df_ind["ANO"] == ano]["AREA"].sum() for ano in anos]

df_comparacao = pd.DataFrame({
    "Ano": anos,
    "Quantidade de Desmatamentos": quantidade_desmatamentos,
    "Area Perdida Total": area_perdida
})

fig = px.bar(df_comparacao, x="Ano", y=["Quantidade de Desmatamentos", "Area Perdida Total"], title="Comparação Anual")
st.plotly_chart(fig)

# Você pode adicionar mais gráficos e informações conforme necessário
