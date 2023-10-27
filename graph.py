# Imports
import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Class Definition
class DeforestationAnalysis:
    def __init__(self):
        self.df_inc, self.df_ind = self.load_data()
        self.sidebar_filters()

    def load_data(self):
        """Load the datasets."""
        df_inc = pd.read_csv("fires.csv", sep=';')
        df_ind = pd.read_csv("dataset_indigenas.csv", sep=';', encoding='latin-1', decimal=',')
        df_inc['year'] = df_inc['date'].str.split('/').str[0].astype(int)
        df_inc.rename(columns={'class': 'Classe'}, inplace=True)
        return df_inc, df_ind

    def sidebar_filters(self):
        """Create sidebar filters."""
        st.sidebar.header("Filtros")
        years = ["Todos"] + sorted(self.df_ind["ANO"].unique().tolist(), reverse=True)
        self.ano_selected = st.sidebar.selectbox("Selecione o ano", years)
        classes = ["Todos"] + self.df_inc["Classe"].unique().tolist()
        self.classe_selected = st.sidebar.multiselect("Selecione as classes de desmatamento", classes, default=["Todos"])
        states = ["Todos"] + self.df_inc["uf"].unique().tolist()
        self.estado_selected = st.sidebar.multiselect("Selecione os estados", states, default=["Todos"])

    def run(self):
        """Main run function to execute the dashboard."""
        st.title("Análise de Desmatamento")

        # Filtering data based on user inputs
        df_inc_filtered = self.filter_inc_data()
        df_ind_selected = self.filter_ind_data()

        # Display plots
        col1, col2 = st.columns(2)
        with col1:
            self.plot_classe_distribution(df_inc_filtered)
        with col2:
            self.plot_state_distribution(df_inc_filtered)
        self.plot_area_by_tribe(df_ind_selected)
        self.plot_annual_comparison(df_inc_filtered, df_ind_selected)

    def filter_inc_data(self):
        """Filter the 'inc' dataset based on user input."""
        df_filtered = self.df_inc.copy()
        if "Todos" not in self.classe_selected:
            df_filtered = df_filtered[df_filtered["Classe"].isin(self.classe_selected)]
        if "Todos" not in self.estado_selected:
            df_filtered = df_filtered[df_filtered["uf"].isin(self.estado_selected)]
        if self.ano_selected != "Todos":
            df_filtered = df_filtered[df_filtered["year"] == int(self.ano_selected)]
        return df_filtered


    def filter_ind_data(self):
        """Filter the 'ind' dataset based on user input."""
        if self.ano_selected != "Todos":
            return self.df_ind[self.df_ind["ANO"] == int(self.ano_selected)]
        else:
            return self.df_ind.copy()

    def plot_classe_distribution(self, df):
        """Plot distribution of deforestation types."""
        if not df.empty:
            fig = px.pie(df, names='Classe', title='Distribuição dos tipos de desmatamento')
            st.plotly_chart(fig)

    def plot_state_distribution(self, df):
        """Plot distribution of deforestation by states."""
        if not df.empty:
            fig = px.pie(df, names='uf', title='Distribuição dos desmatamentos por estado')
            st.plotly_chart(fig)

    def plot_area_by_tribe(self, df):
        """Plot deforested area by tribe."""
        fig = px.bar(df, x='TRIBO', y='AREA', title=f'Área desmatada por tribo em {self.ano_selected}')
        st.plotly_chart(fig)

    def plot_annual_comparison(self, df_inc, df_ind):
        """Plot annual comparison between deforestation quantity and lost area."""
        df_inc_agg = df_inc.groupby("year").size().reset_index(name="Quantidade de Desmatamentos")
        df_ind_agg = df_ind.groupby("ANO")["AREA"].sum().reset_index(name="Area Perdida Total")
        df_comparacao = pd.merge(df_inc_agg, df_ind_agg, left_on="year", right_on="ANO", how="outer").fillna(0)
        df_comparacao.drop(columns="ANO", inplace=True) 
        fig = px.bar(df_comparacao, x="year", y=["Quantidade de Desmatamentos", "Area Perdida Total"], barmode="group", title="Comparação Anual")
        st.plotly_chart(fig)

# Main Execution
if __name__ == '__main__':
    analysis = DeforestationAnalysis()
    analysis.run()
