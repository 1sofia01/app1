import streamlit as st
import requests

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🎵 Global Music Charts",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
GENRES = {
    "Pop":        {"deezer_id": 132, "itunes_id": 14,  "emoji": "🎤", "color": "#FF6B9D"},
    "Rock":       {"deezer_id": 152, "itunes_id": 21,  "emoji": "🎸", "color": "#FF4E50"},
    "Hip Hop":    {"deezer_id": 116, "itunes_id": 18,  "emoji": "🎤", "color": "#9B59B6"},
    "Electronic": {"deezer_id": 106, "itunes_id": 7,   "emoji": "🎧", "color": "#3498DB"},
    "Jazz":       {"deezer_id": 129, "itunes_id": 11,  "emoji": "🎷", "color": "#F39C12"},
    "Classical":  {"deezer_id": 98,  "itunes_id": 5,   "emoji": "🎻", "color": "#1ABC9C"},
    "R&B":        {"deezer_id": 165, "itunes_id": 15,  "emoji": "🎵", "color": "#E67E22"},
    "Sertanejo":  {"deezer_id": 0,   "itunes_id": 0,   "emoji": "🤠", "color": "#27AE60"},
}

COUNTRIES = {
    "🇧🇷 Brasil":       "br",
    "🇺🇸 EUA":          "us",
    "🇬🇧 Reino Unido":  "gb",
    "🇵🇹 Portugal":     "pt",
    "🇦🇷 Argentina":    "ar",
    "🇲🇽 México":       "mx",
    "🇯🇵 Japão":        "jp",
}

MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


# ─────────────────────────────────────────────
# CSS — dark/light mode
# ─────────────────────────────────────────────
def load_css(dark: bool):
    bg       = "#0d0d17" if dark else "#f0f2f6"
    card_bg  = "#16162a" if dark else "#ffffff"
    sidebar  = "#11111f" if dark else "#fafafa"
    text     = "#e8e8f0" if dark else "#111827"
    subtext  = "#8888aa" if dark else "#6b7280"
    border   = "#2a2a45" if dark else "#e5e7eb"
    input_bg = "#1e1e35" if dark else "#f9fafb"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {bg} !important;
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar} !important;
        border-right: 1px solid {border};
    }}
    [data-testid="stSidebar"] * {{ color: {text} !important; }}

    h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; color: {text} !important; }}

    /* ── Music card ── */
    .music-card {{
        background: {card_bg};
        border-radius: 14px;
        padding: 11px 14px;
        margin-bottom: 9px;
        display: flex;
        align-items: center;
        gap: 12px;
        border: 1px solid {border};
        transition: transform 0.18s, box-shadow 0.18s;
    }}
    .music-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.22);
    }}
    .rank-num {{
        font-family: 'Syne', sans-serif;
        font-size: 1.35em;
        font-weight: 800;
        min-width: 38px;
        text-align: center;
        color: {text};
    }}
    .album-thumb {{
        width: 54px;
        height: 54px;
        border-radius: 9px;
        object-fit: cover;
        flex-shrink: 0;
        background: {border};
    }}
    .album-placeholder {{
        width: 54px;
        height: 54px;
        border-radius: 9px;
        background: linear-gradient(135deg, #2a2a45, #1a1a2e);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4em;
        flex-shrink: 0;
    }}
    .track-info {{ flex: 1; overflow: hidden; }}
    .track-title {{
        font-weight: 600;
        color: {text};
        font-size: 0.92em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .track-artist {{
        color: {subtext};
        font-size: 0.8em;
        margin-top: 2px;
    }}
    .source-pill {{
        font-size: 0.68em;
        font-weight: 700;
        letter-spacing: 0.04em;
        padding: 3px 9px;
        border-radius: 20px;
        flex-shrink: 0;
        text-transform: uppercase;
    }}
    .pill-deezer  {{ background: #ff3266; color: #fff; }}
    .pill-itunes  {{ background: #fc3c44; color: #fff; }}

    /* ── Genre header ── */
    .genre-header {{
        font-family: 'Syne', sans-serif;
        font-size: 1.05em;
        font-weight: 700;
        color: {text};
        padding-bottom: 8px;
        border-bottom: 3px solid;
        margin-bottom: 12px;
    }}

    /* ── Section caption ── */
    .section-caption {{
        color: {subtext};
        font-size: 0.82em;
        margin-bottom: 16px;
    }}

    /* ── Welcome screen ── */
    .welcome-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 20px;
        text-align: center;
    }}
    .welcome-icon {{ font-size: 4.5em; margin-bottom: 12px; }}
    .welcome-title {{
        font-family: 'Syne', sans-serif;
        font-size: 2.4em;
        font-weight: 800;
        color: {text};
        margin: 0;
    }}
    .welcome-sub {{ color: {subtext}; margin-top: 10px; font-size: 1.05em; }}

    /* ── Misc overrides ── */
    .stAudio {{ margin-top: -6px; margin-bottom: 4px; }}
    div[data-testid="stTab"] button {{ font-family: 'Syne', sans-serif; font-weight: 600; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# API helpers
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_deezer(genre_name: str, genre_info: dict, limit: int = 5) -> list:
    tracks = []

    # 1️⃣  Official genre chart
    if genre_info["deezer_id"] > 0:
        try:
            url = f"https://api.deezer.com/chart/{genre_info['deezer_id']}/tracks?limit={limit}"
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                items = r.json().get("data", [])
                for i, item in enumerate(items[:limit]):
                    tracks.append({
                        "rank":    i + 1,
                        "title":   item["title"],
                        "artist":  item["artist"]["name"],
                        "cover":   item.get("album", {}).get("cover_medium", ""),
                        "preview": item.get("preview", ""),
                        "source":  "deezer",
                    })
        except Exception:
            pass

    # 2️⃣  Fallback: keyword search
    if not tracks:
        try:
            url = f"https://api.deezer.com/search?q={genre_name}&order=RANKING&limit={limit}"
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                items = r.json().get("data", [])
                for i, item in enumerate(items[:limit]):
                    tracks.append({
                        "rank":    i + 1,
                        "title":   item["title"],
                        "artist":  item["artist"]["name"],
                        "cover":   item.get("album", {}).get("cover_medium", ""),
                        "preview": item.get("preview", ""),
                        "source":  "deezer",
                    })
        except Exception:
            pass

    return tracks


@st.cache_data(ttl=3600)
def fetch_itunes(genre_name: str, genre_info: dict, country: str = "us", limit: int = 5) -> list:
    if genre_info["itunes_id"] == 0:
        return []
    tracks = []
    try:
        url = (
            f"https://itunes.apple.com/{country}/rss/topsongs/"
            f"limit={max(limit, 10)}/genre={genre_info['itunes_id']}/json"
        )
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            entries = r.json().get("feed", {}).get("entry", [])
            for i, entry in enumerate(entries[:limit]):
                title  = entry.get("im:name", {}).get("label", "Unknown")
                artist = entry.get("im:artist", {}).get("label", "Unknown")
                images = entry.get("im:image", [])
                cover  = images[-1]["label"].replace("55x55bb", "100x100bb") if images else ""
                tracks.append({
                    "rank":    i + 1,
                    "title":   title,
                    "artist":  artist,
                    "cover":   cover,
                    "preview": "",
                    "source":  "itunes",
                })
    except Exception:
        pass
    return tracks


@st.cache_data(ttl=600)
def search_deezer(query: str, limit: int = 10) -> list:
    try:
        url = f"https://api.deezer.com/search?q={query}&order=RANKING&limit={limit}"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            items = r.json().get("data", [])
            return [
                {
                    "rank":    i + 1,
                    "title":   item["title"],
                    "artist":  item["artist"]["name"],
                    "cover":   item.get("album", {}).get("cover_medium", ""),
                    "preview": item.get("preview", ""),
                    "source":  "deezer",
                }
                for i, item in enumerate(items[:limit])
            ]
    except Exception:
        return []
    return []


# ─────────────────────────────────────────────
# UI component
# ─────────────────────────────────────────────
def track_card(track: dict, show_preview: bool = True):
    rank   = track["rank"]
    medal  = MEDALS.get(rank, f"#{rank}")
    src    = track["source"]
    pill   = f'<span class="source-pill pill-{src}">{"Deezer" if src=="deezer" else "iTunes"}</span>'
    cover  = track.get("cover", "")

    if cover:
        img_html = f'<img src="{cover}" class="album-thumb">'
    else:
        emoji = "🎵"
        img_html = f'<div class="album-placeholder">{emoji}</div>'

    st.markdown(f"""
    <div class="music-card">
        <div class="rank-num">{medal}</div>
        {img_html}
        <div class="track-info">
            <div class="track-title">{track["title"]}</div>
            <div class="track-artist">{track["artist"]}</div>
        </div>
        {pill}
    </div>
    """, unsafe_allow_html=True)

    if show_preview and track.get("preview"):
        st.audio(track["preview"], format="audio/mp3")


def genre_column(genre: str, tracks: list, show_preview: bool):
    info  = GENRES[genre]
    color = info["color"]
    emoji = info["emoji"]
    st.markdown(
        f'<div class="genre-header" style="border-color:{color}">{emoji} {genre}</div>',
        unsafe_allow_html=True,
    )
    if tracks:
        for t in tracks:
            track_card(t, show_preview)
    else:
        st.error("Sem dados para este gênero.")


# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────
def main():
    # ── Sidebar ──────────────────────────────
    with st.sidebar:
        st.markdown("### 🎵 Music Charts")
        st.divider()

        nome = st.text_input("👤 Seu Nome:", placeholder="Digite seu nome...")
        dark = st.toggle("🌙 Modo Escuro", value=True)

        st.divider()
        st.markdown("**🌍 País (iTunes)**")
        pais_nome = st.selectbox("País:", list(COUNTRIES.keys()), label_visibility="collapsed")
        pais_code = COUNTRIES[pais_nome]

        st.divider()
        st.markdown("**🎸 Gêneros**")
        selected = st.multiselect(
            "Selecione:",
            list(GENRES.keys()),
            default=["Pop", "Rock", "Hip Hop"],
            label_visibility="collapsed",
        )

        limit        = st.slider("Músicas por gênero:", 3, 10, 5)
        show_preview = st.checkbox("▶️ Preview (Deezer)", value=True)

        st.divider()
        st.caption("Fontes: Deezer Public API + Apple iTunes RSS\nRankings atualizados a cada 1h")

    # ── CSS ──────────────────────────────────
    load_css(dark)

    # ── Welcome screen ───────────────────────
    if not nome:
        st.markdown("""
        <div class="welcome-wrap">
            <div class="welcome-icon">🎵</div>
            <p class="welcome-title">Global Music Charts</p>
            <p class="welcome-sub">Digite seu nome na barra lateral para começar</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Header ───────────────────────────────
    st.markdown(f"# 🎵 Olá, {nome}!")
    st.markdown(
        f'<p class="section-caption">📡 Deezer API &amp; iTunes RSS &nbsp;|&nbsp; '
        f'🌍 {pais_nome} &nbsp;|&nbsp; 🔄 Cache de 1h</p>',
        unsafe_allow_html=True,
    )

    if not selected:
        st.warning("⚠️ Selecione pelo menos um gênero na barra lateral.")
        return

    # ── Tabs ─────────────────────────────────
    tab_deezer, tab_itunes, tab_search = st.tabs(
        ["🟥 Deezer Charts", "🍎 iTunes Charts", "🔍 Busca Livre"]
    )

    # ── DEEZER ───────────────────────────────
    with tab_deezer:
        st.markdown(
            '<p class="section-caption">Top músicas por gênero — Deezer (ranking real, com preview)</p>',
            unsafe_allow_html=True,
        )
        ncols = min(len(selected), 3)
        rows  = [selected[i : i + ncols] for i in range(0, len(selected), ncols)]

        for row in rows:
            cols = st.columns(len(row))
            for col, genre in zip(cols, row):
                with col:
                    with st.spinner(f"Buscando {genre}…"):
                        tracks = fetch_deezer(genre, GENRES[genre], limit)
                    genre_column(genre, tracks, show_preview)

    # ── ITUNES ───────────────────────────────
    with tab_itunes:
        st.markdown(
            f'<p class="section-caption">Top músicas por gênero — iTunes ({pais_nome})</p>',
            unsafe_allow_html=True,
        )
        ncols = min(len(selected), 3)
        rows  = [selected[i : i + ncols] for i in range(0, len(selected), ncols)]

        for row in rows:
            cols = st.columns(len(row))
            for col, genre in zip(cols, row):
                with col:
                    if GENRES[genre]["itunes_id"] == 0:
                        st.markdown(
                            f'<div class="genre-header" style="border-color:{GENRES[genre]["color"]}">'
                            f'{GENRES[genre]["emoji"]} {genre}</div>',
                            unsafe_allow_html=True,
                        )
                        st.info("Gênero não disponível no iTunes por categoria.")
                        continue
                    with st.spinner(f"Buscando {genre}…"):
                        tracks = fetch_itunes(genre, GENRES[genre], pais_code, limit)
                    genre_column(genre, tracks, show_preview=False)

    # ── BUSCA LIVRE ──────────────────────────
    with tab_search:
        st.markdown(
            '<p class="section-caption">Pesquise qualquer artista ou música — powered by Deezer</p>',
            unsafe_allow_html=True,
        )
        query = st.text_input(
            "🔍 Pesquisar:",
            placeholder="ex: The Weeknd, Blinding Lights, Taylor Swift…",
            label_visibility="visible",
        )

        if query.strip():
            with st.spinner("Buscando…"):
                results = search_deezer(query.strip(), limit=10)

            if results:
                c1, c2 = st.columns(2)
                for i, track in enumerate(results):
                    with (c1 if i % 2 == 0 else c2):
                        track_card(track, show_preview)
            else:
                st.error("Nenhum resultado encontrado.")
        else:
            st.info("💡 Use a caixa acima para pesquisar qualquer música ou artista.")

    # ── Footer ───────────────────────────────
    st.divider()
    st.caption(
        "🎵 Dados via **Deezer Public API** & **Apple iTunes RSS Feed** · "
        "Rankings baseados em popularidade real · Preview 30s via Deezer"
    )


if __name__ == "__main__":
    main()
