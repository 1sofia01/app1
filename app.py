import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Music Top 3 por Gênero", page_icon="🎵", layout="wide")

# Estilização Personalizada
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stHeader { color: #1DB954; }
    .music-card {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎵 Descoberta Musical: Top 3 por Gênero")
    st.subheader("Identifique-se para ver as músicas mais ouvidas do momento")

    # Área de Identificação do Usuário
    with st.sidebar:
        st.header("👤 Identificação")
        nome_usuario = st.text_input("Digite seu nome ou ID de usuário:")
        plataforma = st.selectbox("Escolha a plataforma:", ["Spotify", "Deezer", "Apple Music"])
        
        if nome_usuario:
            st.success(f"Logado como: {nome_usuario}")

    if not nome_usuario:
        st.info("💡 Por favor, identifique-se na barra lateral para carregar os dados da API simulada.")
        st.stop()

    # Simulação de dados de uma API (Em um cenário real, você usaria 'requests' ou 'spotipy')
    @st.cache_data
    def buscar_top_musicas_api():
        data = {
            "Gênero": ["Pop", "Pop", "Pop", "Rock", "Rock", "Rock", "Sertanejo", "Sertanejo", "Sertanejo", "Jazz", "Jazz", "Jazz"],
            "Música": [
                "Flowers", "As It Was", "Anti-Hero", 
                "Lux Æterna", "Rescued", "Lost",
                "Erro Gostoso", "Nosso Quadro", "Leão",
                "The Nearness of You", "Blue World", "Don't Know Why"
            ],
            "Artista": [
                "Miley Cyrus", "Harry Styles", "Taylor Swift",
                "Metallica", "Foo Fighters", "Linkin Park",
                "Simone Mendes", "Ana Castela", "Marília Mendonça",
                "Norah Jones", "Mac Miller", "Norah Jones"
            ],
            "Ouvintes (Mi)": [120, 115, 110, 45, 42, 40, 95, 92, 90, 15, 12, 10]
        }
        return pd.DataFrame(data)

    st.write(f"### Olá, **{nome_usuario}**! Aqui estão os destaques de hoje na **{plataforma}**:")

    df_musicas = buscar_top_musicas_api()
    generos = df_musicas["Gênero"].unique()

    # Layout de colunas para os gêneros
    cols = st.columns(len(generos))

    for i, genero in enumerate(generos):
        with cols[i]:
            st.markdown(f"### {genero}")
            top_3 = df_musicas[df_musicas["Gênero"] == genero].head(3)
            
            for index, row in top_3.iterrows():
                st.markdown(f"""
                <div class="music-card">
                    <strong>{row['Música']}</strong><br>
                    <small>{row['Artista']}</small>
                </div>
                """, unsafe_allow_html=True)
                
    # Visualização de Dados
    st.divider()
    st.write("### 📊 Popularidade por Gênero (Ouvintes em Milhões)")
    st.bar_chart(df_musicas.groupby("Gênero")["Ouvintes (Mi)"].sum())

if __name__ == "__main__":
    main()
