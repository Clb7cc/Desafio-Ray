import streamlit as st
import plotly.express as px
from aplicacao import listar_videos_playlist, obter_detalhes_videos, ID_PLAYLIST
import pandas as pd

st.set_page_config(page_title="Destaques F1 2024", layout="wide")
st.title("🏎️ Destaques da F1 2024 - Dashboard")

@st.cache_data
def carregar_dados():
    st.info("Carregando dados da playlist...")
    ids_videos = listar_videos_playlist(ID_PLAYLIST)
    dataframe = obter_detalhes_videos(ids_videos)
    dataframe['data_publicacao'] = pd.to_datetime(dataframe['data_publicacao'])
    st.success("Dados carregados com sucesso!")
    return dataframe

df = carregar_dados()

# Sidebar com informações gerais
with st.sidebar:
    st.header("📊 Estatísticas da Playlist")
    st.metric("Total de Vídeos", len(df))
    st.metric("Visualizações Totais", f"{df['visualizacoes'].sum():,}")
    st.metric("Média de Visualizações", f"{df['visualizacoes'].mean():,.0f}")
    st.metric("Vídeo Mais Recente", df['data_publicacao'].max().strftime('%d/%m/%Y'))
    
    # Filtros
    st.header("🔍 Filtros")
    visualizacoes_min = st.slider(
        "Visualizações Mínimas", 
        min_value=0, 
        max_value=int(df['visualizacoes'].max()), 
        value=0
    )
    
    data_inicio = st.date_input(
        "Data Início",
        value=df['data_publicacao'].min().date()
    )
    data_fim = st.date_input(
        "Data Fim", 
        value=df['data_publicacao'].max().date()
    )

# Aplicacao dos filtros
df_filtrado = df[
    (df['visualizacoes'] >= visualizacoes_min) &
    (df['data_publicacao'].dt.date >= data_inicio) &
    (df['data_publicacao'].dt.date <= data_fim)
]

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Evolução das Visualizações ao Longo do Tempo")
    
    # Gráfico de dispersão
    fig = px.scatter(
        df_filtrado, 
        x='data_publicacao', 
        y='visualizacoes', 
        hover_data=['titulo'],
        size='visualizacoes',
        title='Visualizações por Data de Publicação',
        labels={
            'data_publicacao': 'Data de Publicação',
            'visualizacoes': 'Visualizações',
            'titulo': 'Título do Vídeo'
        }
    )
    fig.update_traces(marker=dict(opacity=0.7))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top 5 Vídeos")
    top_5 = df_filtrado.nlargest(5, 'visualizacoes')
    for i, (_, video) in enumerate(top_5.iterrows(), 1):
        with st.container():
            st.markdown(f"**#{i} - {video['titulo'][:30]}...**")
            st.metric("Visualizações", f"{video['visualizacoes']:,}")
            st.progress(video['visualizacoes'] / top_5['visualizacoes'].max())
            st.markdown("---")

with col1:
    st.subheader("📈 Engajamento dos Mais Recentes")
    recentes = df_filtrado.sort_values('data_publicacao', ascending=False).head(5)
    fig2 = px.bar(
        recentes, 
        x='curtidas', 
        y='titulo', 
        orientation='h', 
        title='Curtidas nos Vídeos Mais Recentes'
    )
    st.plotly_chart(fig2, use_container_width=True)


st.subheader("📋 Top 10 Vídeos por Visualizações")
top_10 = df_filtrado.sort_values('visualizacoes', ascending=False).head(10)

tabela_formatada = top_10[[
    'titulo', 
    'data_publicacao', 
    'visualizacoes', 
    'curtidas', 
    'comentarios'
]].copy()
tabela_formatada['data_publicacao'] = tabela_formatada['data_publicacao'].dt.strftime('%d/%m/%Y')
tabela_formatada['visualizacoes'] = tabela_formatada['visualizacoes'].apply(lambda x: f"{x:,}")
tabela_formatada['curtidas'] = tabela_formatada['curtidas'].apply(lambda x: f"{x:,}" if pd.notna(x) else "N/A")
tabela_formatada['comentarios'] = tabela_formatada['comentarios'].apply(lambda x: f"{x:,}" if pd.notna(x) else "N/A")

tabela_formatada.columns = [
    'Título', 
    'Data Publicação', 
    'Visualizações', 
    'Curtidas', 
    'Comentários'
]

st.dataframe(
    tabela_formatada,
    use_container_width=True,
    height=400
)