import streamlit as st
import pandas as pd
import requests

# Configuração da página
st.set_page_config(page_title="Music Top 3 por Gênero", page_icon="🎵", layout="wide")

# Estilização
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .music-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 6px solid #ef5464;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .genre-title {
        color: #333;
        font-weight: bold;
        border-bottom: 2px solid #ef5464;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=3600) # Cache de 1 hora
def buscar_musicas_deezer(genero):
    """Busca músicas na API gratuita do Deezer por gênero."""
    try:
        url = f"https://api.deezer.com/search?q=genre:\"{genero}\"&order=RANKING"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            songs = []
            # Pegamos os top 3 resultados válidos
            for item in data.get('data', [])[:3]:
                songs.append({
                    "Música": item['title'],
                    "Artista": item['artist']['name'],
                    "Rank": item['rank'],
                    "Preview": item['preview']
                })
            return songs
        return []
    except Exception as e:
        return []

def main():
    st.title("🎵 Top 3 Músicas por Gênero (API Real)")
    
    with st.sidebar:
        st.header("👤 Identificação")
        nome_usuario = st.text_input("Seu Nome:")
        
        # Lista de gêneros populares para consulta
        generos_interesse = ["Pop", "Rock", "Sertanejo", "Jazz", "Electronic", "Hip Hop"]
        selecao_generos = st.multiselect("Selecione os gêneros:", generos_interesse, default=["Pop", "Rock", "Jazz"])

    if not nome_usuario:
        st.info("👋 Olá! Insira seu nome na barra lateral para carregar as músicas da API do Deezer.")
        st.stop()

    st.write(f"### Bem-vindo, **{nome_usuario}**! Buscando as tendências mundiais...")

    if not selecao_generos:
        st.warning("Selecione pelo menos um gênero musical.")
    else:
        # Layout de colunas
        cols = st.columns(len(selecao_generos))
        
        for i, genero in enumerate(selecao_generos):
            with cols[i]:
                st.markdown(f"<div class='genre-title'>🎸 {genero}</div>", unsafe_allow_html=True)
                
                with st.spinner(f"Lendo {genero}..."):
                    musicas = buscar_musicas_deezer(genero)
                
                if musicas:
                    for music in musicas:
                        st.markdown(f"""
                        <div class="music-card">
                            <div style="font-size: 1.1em; color: #ef5464;"><strong>{music['Música']}</strong></div>
                            <div style="color: #666;">{music['Artista']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        # Opcional: Adiciona o player de preview da música
                        st.audio(music['Preview'], format="audio/mp3")
                else:
                    st.error("Nenhum dado encontrado.")

    st.divider()
    st.caption("Dados fornecidos via API Pública do Deezer. O ranking é baseado na popularidade atual da plataforma.")

if __name__ == "__main__":
    main()
