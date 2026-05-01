"""
Dashboard Político do Brasil — Streamlit App
Requer: streamlit, plotly, pandas, geopandas, requests
Instale com: pip install streamlit plotly pandas geopandas requests
Execute com: streamlit run brasil_politico.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import requests

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Brasil Político",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }
    .metric-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    .metric-title {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #7d8590;
        margin-bottom: 6px;
    }
    .metric-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: #58a6ff;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #7d8590;
        margin-top: 4px;
    }
    h1 { color: #e6edf3 !important; }
    h2, h3 { color: #cdd9e5 !important; }
    .stSidebar { background: #161b22 !important; }
    .stSidebar [data-testid="stSidebarContent"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label { color: #cdd9e5 !important; }
    .section-divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 2rem 0;
    }
    .tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DADOS — ESTATÍSTICAS POLÍTICAS POR ESTADO
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    dados = {
        "Estado": [
            "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará",
            "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão",
            "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará",
            "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro",
            "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima",
            "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
        ],
        "Sigla": [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
            "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ],
        "Vereadores": [
            855, 2890, 680, 3100, 11200, 5760, 24, 1890, 4620, 4870,
            3200, 2510, 19800, 5120, 3200, 7640, 5520, 3010, 5040,
            2780, 6380, 1870, 630, 4560, 25100, 1520, 1890
        ],
        "Prefeitos_Alinhados": [
            68, 72, 55, 61, 59, 64, 100, 70, 66, 71,
            58, 62, 67, 63, 69, 72, 65, 70, 58,
            66, 71, 60, 57, 74, 63, 68, 65
        ],
        "Indice_Gov": [  # índice fictício de governabilidade 0–100
            62, 55, 58, 60, 67, 63, 81, 72, 70, 53,
            65, 68, 74, 57, 61, 76, 64, 56, 59,
            62, 73, 61, 57, 79, 78, 60, 63
        ],
        "Partido_Gov": [
            "PT", "União", "PDT", "PL", "PT", "PT", "PL", "PL", "PSD", "PSD",
            "PL", "PSD", "PSD", "União", "PT", "PL", "PT", "PT", "PL",
            "PSD", "PL", "PL", "PL", "PL", "PSD", "PSD", "PSD"
        ],
        "Eleitorado_M": [  # em milhões
            0.6, 2.4, 0.6, 2.5, 12.1, 6.8, 2.2, 3.2, 5.1, 4.5,
            2.6, 2.1, 16.3, 6.3, 3.1, 9.2, 7.1, 2.5, 13.2,
            2.5, 8.8, 1.3, 0.4, 5.9, 35.0, 1.7, 1.2
        ],
        "IDH": [
            0.663, 0.683, 0.708, 0.674, 0.660, 0.682, 0.824, 0.740, 0.735, 0.639,
            0.725, 0.729, 0.731, 0.646, 0.683, 0.749, 0.673, 0.655, 0.711,
            0.684, 0.746, 0.690, 0.707, 0.774, 0.783, 0.665, 0.699
        ],
    }
    return pd.DataFrame(dados)


@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None


df = load_data()
geojson = load_geojson()

# Mapeamento partido → cor
cores_partido = {
    "PT": "#e53935",
    "PL": "#1565c0",
    "PSD": "#388e3c",
    "União": "#f57c00",
    "PDT": "#6a1b9a",
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗳️ Filtros")
    st.markdown("<hr style='border-color:#30363d'>", unsafe_allow_html=True)

    partidos_disponiveis = sorted(df["Partido_Gov"].unique())
    partidos_sel = st.multiselect(
        "Partido do Governador",
        partidos_disponiveis,
        default=partidos_disponiveis,
    )

    metrica_mapa = st.selectbox(
        "Métrica no Mapa",
        options=["Indice_Gov", "IDH", "Eleitorado_M", "Vereadores"],
        format_func=lambda x: {
            "Indice_Gov": "Índice de Governabilidade",
            "IDH": "IDH",
            "Eleitorado_M": "Eleitorado (milhões)",
            "Vereadores": "Nº de Vereadores",
        }[x],
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#7d8590; font-size:0.72rem; line-height:1.7;'>
    ⚠️ Dados ilustrativos para fins de visualização. 
    Não representam informações oficiais.
    </div>
    """, unsafe_allow_html=True)

df_filtrado = df[df["Partido_Gov"].isin(partidos_sel)]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("# 🇧🇷 Dashboard Político do Brasil")
st.markdown(
    "<p style='color:#7d8590; margin-top:-0.5rem; margin-bottom:1.5rem;'>"
    "Panorama político-eleitoral dos estados brasileiros</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# MÉTRICAS RÁPIDAS
# ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
metricas = [
    ("Estados", f"{len(df_filtrado)}", "filtrados"),
    ("Eleitorado Total", f"{df_filtrado['Eleitorado_M'].sum():.1f}M", "eleitores"),
    ("Índice Gov. Médio", f"{df_filtrado['Indice_Gov'].mean():.0f}", "/ 100 pts"),
    ("IDH Médio", f"{df_filtrado['IDH'].mean():.3f}", "média ponderada"),
]
for col, (titulo, valor, sub) in zip([col1, col2, col3, col4], metricas):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAPA COROPLÉTICO
# ─────────────────────────────────────────────
col_mapa, col_pizza = st.columns([2, 1])

with col_mapa:
    st.markdown("### 🗺️ Mapa por Estado")

    label_metrica = {
        "Indice_Gov": "Índice de Governabilidade",
        "IDH": "IDH",
        "Eleitorado_M": "Eleitorado (M)",
        "Vereadores": "Nº Vereadores",
    }[metrica_mapa]

    if geojson:
        fig_mapa = px.choropleth(
            df_filtrado,
            geojson=geojson,
            locations="Sigla",
            featureidkey="properties.sigla",
            color=metrica_mapa,
            color_continuous_scale="Blues",
            labels={metrica_mapa: label_metrica},
            hover_name="Estado",
            hover_data={
                "Sigla": False,
                "Partido_Gov": True,
                "IDH": True,
                "Eleitorado_M": ":.1f",
                metrica_mapa: True,
            },
        )
        fig_mapa.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor="#0d1117",
        )
        fig_mapa.update_layout(
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            font_color="#e6edf3",
            margin=dict(l=0, r=0, t=10, b=0),
            height=420,
            coloraxis_colorbar=dict(
                bgcolor="#161b22",
                tickcolor="#7d8590",
                title_font_color="#cdd9e5",
            ),
        )
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning("GeoJSON não pôde ser carregado. Verifique a conexão.")
        fig_bar_alt = px.bar(
            df_filtrado.sort_values(metrica_mapa, ascending=True).tail(15),
            x=metrica_mapa, y="Sigla",
            orientation="h",
            color=metrica_mapa,
            color_continuous_scale="Blues",
            labels={metrica_mapa: label_metrica, "Sigla": "Estado"},
        )
        fig_bar_alt.update_layout(
            paper_bgcolor="#161b22", plot_bgcolor="#161b22",
            font_color="#e6edf3", height=420,
        )
        st.plotly_chart(fig_bar_alt, use_container_width=True)

with col_pizza:
    st.markdown("### 🏛️ Governadores por Partido")
    contagem = df_filtrado["Partido_Gov"].value_counts().reset_index()
    contagem.columns = ["Partido", "Estados"]

    cores = [cores_partido.get(p, "#7d8590") for p in contagem["Partido"]]

    fig_pizza = go.Figure(go.Pie(
        labels=contagem["Partido"],
        values=contagem["Estados"],
        marker=dict(colors=cores, line=dict(color="#0d1117", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#e6edf3", size=13),
        hovertemplate="<b>%{label}</b><br>%{value} estado(s)<br>%{percent}<extra></extra>",
        hole=0.45,
    ))
    fig_pizza.update_layout(
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        font_color="#e6edf3",
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            bgcolor="#1c2333",
            bordercolor="#30363d",
            borderwidth=1,
            font_color="#cdd9e5",
        ),
        annotations=[dict(
            text="<b>Gov.</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#7d8590"),
        )],
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SCATTER IDH × GOVERNABILIDADE
# ─────────────────────────────────────────────
col_scatter, col_bar = st.columns([3, 2])

with col_scatter:
    st.markdown("### 📊 IDH × Índice de Governabilidade")
    fig_scatter = px.scatter(
        df_filtrado,
        x="IDH",
        y="Indice_Gov",
        color="Partido_Gov",
        size="Eleitorado_M",
        text="Sigla",
        color_discrete_map=cores_partido,
        labels={
            "IDH": "IDH",
            "Indice_Gov": "Índice de Governabilidade",
            "Partido_Gov": "Partido",
            "Eleitorado_M": "Eleitorado (M)",
        },
        hover_data={"Estado": True, "Sigla": False},
    )
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=10, color="#cdd9e5"),
        marker=dict(opacity=0.85, line=dict(width=1, color="#30363d")),
    )
    fig_scatter.update_layout(
        paper_bgcolor="#161b22",
        plot_bgcolor="#1c2333",
        font_color="#e6edf3",
        height=360,
        xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
        legend=dict(bgcolor="#1c2333", bordercolor="#30363d", borderwidth=1),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_bar:
    st.markdown("### 🗳️ Eleitorado por Partido")
    eleitorado_partido = (
        df_filtrado.groupby("Partido_Gov")["Eleitorado_M"]
        .sum()
        .reset_index()
        .sort_values("Eleitorado_M", ascending=True)
    )
    cores_bar = [cores_partido.get(p, "#7d8590") for p in eleitorado_partido["Partido_Gov"]]
    fig_bar = go.Figure(go.Bar(
        x=eleitorado_partido["Eleitorado_M"],
        y=eleitorado_partido["Partido_Gov"],
        orientation="h",
        marker=dict(color=cores_bar, line=dict(width=0)),
        text=eleitorado_partido["Eleitorado_M"].apply(lambda v: f"{v:.1f}M"),
        textposition="outside",
        textfont=dict(color="#cdd9e5", size=12),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}M eleitores<extra></extra>",
    ))
    fig_bar.update_layout(
        paper_bgcolor="#161b22",
        plot_bgcolor="#1c2333",
        font_color="#e6edf3",
        height=360,
        xaxis=dict(gridcolor="#21262d", title="Eleitorado (milhões)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=40, t=10, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABELA DETALHADA
# ─────────────────────────────────────────────
st.markdown("### 📋 Tabela Detalhada")

df_exibir = df_filtrado[["Estado", "Sigla", "Partido_Gov", "IDH", "Indice_Gov", "Eleitorado_M", "Vereadores"]].copy()
df_exibir.columns = ["Estado", "UF", "Partido Gov.", "IDH", "Gov. (%)", "Eleitorado (M)", "Vereadores"]
df_exibir = df_exibir.sort_values("Estado")

st.dataframe(
    df_exibir.style
        .background_gradient(subset=["IDH"], cmap="Blues")
        .background_gradient(subset=["Gov. (%)"], cmap="Greens")
        .format({"IDH": "{:.3f}", "Eleitorado (M)": "{:.1f}", "Gov. (%)": "{:.0f}"}),
    use_container_width=True,
    height=340,
)

# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#484f58; font-size:0.75rem; padding: 1rem 0;'>
    Dashboard Político do Brasil · Dados ilustrativos · Desenvolvido com Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
