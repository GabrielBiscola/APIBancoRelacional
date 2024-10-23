import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
# import get_mysql_data
from query import conexao

query = "SELECT * FROM tb_carros"

df = conexao(query)

if st.button("Atualizar Dados"):
    df = conexao(query)

st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", options=df["marca"].unique(),
                               default=df["marca"].unique())

modelo = st.sidebar.multiselect("Modelo Selecionado", options=df["nome"].unique(),
                               default=df["nome"].unique())

ano = st.sidebar.multiselect("Ano Selecionado", options=df["ano"].unique(),
                               default=df["ano"].unique())

valor = st.sidebar.multiselect("Ano Selecionado", options=df["valor"].unique(),
                               default=df["valor"].unique())

numero_vendas = st.sidebar.multiselect("numero_vendas", options=df["numero_vendas"].unique(),
                               default=df["numero_vendas"].unique())

cor = st.sidebar.multiselect("Cor Selecionada", options=df["cor"].unique(),
                               default=df["cor"].unique())

df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["nome"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["numero_vendas"].isin(numero_vendas)) &
    (df["cor"].isin(cor))
]

def Home():
    with st.expander('Valores'): # Cria uma caixa expansivel com um titulo
        mostrarDados = st.multiselect('Filter: ', df_selecionado, default=[])
        
        # Verifica se o usuario selecionou uma coluna para exibir
        if mostrarDados:
            # Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
    
    if not df_selecionado.empty:
        venda_total =  df_selecionado['numero_vendas'].sum()
        venda_media = df_selecionado['numero_vendas'].mean()
        venda_mediana = df_selecionado['numero_vendas'].median()
        
        # Cria tres colunas para exibir os totais calculados
        total1, total2, total3 = st.columns(3, gap='large')
        
        with total1:
            st.info('Valor total de vendas dos carros', icon='📌')
            st.metric(label='Total', value=f'{venda_total:,.0f}')
            
        with total2:
            st.info('Valor médio das vendas', icon='📌')
            st.metric(label='Média', value=f'{venda_media:,.0f}')
            
        with total3:
            st.info('Valor mediana dos carros', icon='📌')
            st.metric(label='Mediana', value=f'{venda_mediana:,.0f}')
    
    else:
        st.warning('Nenhum dado disponível com os filtros selecionados')
    
    st.markdown('''--------''')   
    
    
# Graficos

def graficos(df_selecionado):
    # Verifica se o dataframe está vazio
    if df_selecionado.empty:
        st.warning('Nenhum dado disponível para gerar gráficos')
        return
    
    graf1, graf2, graf3, graf4, graf5 = st.tabs(['Gráfico de Barras', 'Gráfico de Linhas', 'Gráfico de Pizza', 'Gráfico de Dispersão', 'Gráfico de Área'])

    with graf1:
        st.write("Gráfico de Barras") # Titulo
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        fig_valores = px.bar(investimento,
                             x=investimento.index,
                             y="valor",
                             orientation="h",
                             title="<b>Valores de Carros</b>",
                             color_discrete_sequence=["#0083b3"])
        
        st.plotly_chart(fig_valores, use_container_width=True)

    with graf2:
        st.write("Gráfico de Linhas") 
        dados = df_selecionado.groupby("marca").count()[["valor"]]

        fig_valores2 = px.line(dados,
                            x=dados.index,
                            y="valor",
                            title="<b>Valores por Marca</b>",
                            color_discrete_sequence=["#0083b3"])
        
        st.plotly_chart(fig_valores2, use_container_width=True)

    with graf3:
        st.write("Gráfico de Pizza") 
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_valores3 = px.pie(dados2,
                            values="valor",
                            names=dados2.index,
                            title="<b>Distribuição de valores por Marca</b>")
        
        st.plotly_chart(fig_valores3, use_container_width=True)

    with graf4:
        st.write("Gráfico de Dispersão") 
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])

        fig_valores4 = px.scatter(dados3,
                            x="marca",
                            y="value",
                            color="variable",
                            title="<b>Disperção de valores por Marca</b>")
        
        st.plotly_chart(fig_valores4, use_container_width=True)

    with graf5:
        st.write("Gráfico de Área")

        dados4 = df_selecionado.groupby('ano').size().reset_index(name='total_carros')

        fig_valores5 = px.area(
            dados4,
            x="ano",
            y="total_carros",
            title="<b>Total de Carros por Ano (Gráfico de Área)</b>",
            labels={'total_carros': 'Total de Carros', 'ano': 'Ano'})

        st.plotly_chart(fig_valores5, use_container_width=True)


    
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 20000
    percentual = round((valorAtual / objetivo * 100))

    if percentual > 100:
        st.subheader("Valores Atingidos!!!")
    else:
        st.write(f"Você tem {percentual}% de {objetivo}.")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home",
                                  "Progresso"], icons=["house", "eye"], menu_icon="cast",
                                  default_index=0)
        
        if selecionado == "Home":
            st.subheader(f"Página:{selecionado}")
            Home()
            graficos(df_selecionado)

        if selecionado == "Progresso":
            st.subheader(f"Página:{selecionado}")
            barraprogresso()
            graficos(df_selecionado)

menuLateral()