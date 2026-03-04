import streamlit as st
import sqlite3
import pandas as pd

from scraper import search_and_save

# Configurando a página
st.set_page_config(page_title="Monitor de Preços ML", page_icon="🛒", layout="wide")

DB_PATH = "data/preços.db"

def carregar_dados():
    """
    Lê o banco de dados e retorna um DataFrame do Pandas
    """

    try:
        conn = sqlite3.connect(DB_PATH)

        query = '''
            SELECT p.titulo AS Produto, p.url, h.preco, h.data_hora 
            FROM produtos p
            JOIN historico_precos h ON p.id = h.produto_id
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()

        if not df.empty:
            df['data_hora'] = pd.to_datetime(df['data_hora'])

        return df
    
    except sqlite3.Error as e:
        st.error(f"Erro ao ler o banco de dados: {e}")
        return pd.DataFrame()
    
# ==========================================
# CONSTRUÇÃO DA INTERFACE VISUAL
# ==========================================

st.title(" Dashboard: Monitor de Preços - Mercado Livre")

# 1. Área de pesquisa ( Onde a mágiva do scraper acontece)
st.markdown("Buscar e Adicionar novos produtos")

# Dividindo a tela em duas colunas (uma larga para o texto e uma menor para o botão)
col_input, col_btn = st.columns([3,1])

with col_input:
    termo_busca = st.text_input("O que você quer monitorar no Mercado Livre?", placeholder="Ex: monitor gamer, teclado mecanico...")

with col_btn:
    st.write("") # Espaço em branco para alinhar o botão com a caixa de texto

    # Se o botão for clicado...
    if st.button("Pesquisar e Extrair", use_container_width=True):
        if termo_busca:
            # Mostra uma rodinha de carregamento enquanto o scraper roda
            with st.spinner(f"Buscando '{termo_busca}' no Mercado Livre. Isso pode levar alguns segundos..."):

                # Chama a função !
                search_and_save(termo_busca)

            st.success("Produtos extraídos e salvos no banco de dados com sucesso!")
        else:
            st.warning("Por favor, digite um termo para pesquisar.")

st.divider()

# 2. Área do dashboard (Lendo os dados)

df = carregar_dados()

if df.empty:
    st.info("O banco de dados está vazio ou aguardando dados.")
else:
    # Filtro lateral
    st.sidebar.header("Filtros de Análise")
    produtos_unicos = df['Produto'].unique()
    produto_selecionado = st.sidebar.selectbox("Selecione um produto:", produtos_unicos)

    # Filtra os dados apenas para o produto escolhido
    df_filtrado = df[df['Produto'] == produto_selecionado].copy()
    df_filtrado = df_filtrado.sort_values(by='data_hora')

    # Cálculo dos cards
    preco_atual = df_filtrado.iloc[-1]['preco']
    menor_preco = df_filtrado['preco'].min()
    maior_preco = df_filtrado['preco'].max()

    st.subheader(f"EVOLUÇÃO : {produto_selecionado}")
    url_produto = df_filtrado.iloc[0]['url']
    st.markdown(f"[ Acessar página do produto no Mercado Livre]({url_produto})")

    # Cards de Métricas
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label= "Preço Atual", value=f"R$ {preco_atual:,.2f}")

    with c2:
        delta_menor = None if preco_atual == menor_preco else f"R$ {(preco_atual - menor_preco):,.2f} acima do mínimo"
        st.metric(label="Menor preço historico", value=f"R$ {menor_preco:,.2f}", delta=delta_menor, delta_color="inverse")

    with c3:
        st.metric(label="Maior preço Histórico",  value=f"R$ {maior_preco:,.2f}")

    # Gráfico de Linha
    st.line_chart(df_filtrado.set_index('data_hora')[['preco']], y='preco')