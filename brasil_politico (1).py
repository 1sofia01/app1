"""
╔══════════════════════════════════════════════════════════╗
║       BRASIL POLÍTICO — Dashboard de Análise Eleitoral   ║
║       Desenvolvido com Streamlit + Plotly                ║
╚══════════════════════════════════════════════════════════╝

Dependências (requirements.txt):
    streamlit
    plotly
    pandas
    requests
    matplotlib

Executar: streamlit run brasil_politico.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════
# CONFIGURAÇÃO GLOBAL
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Brasil Político",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# ESTILOS GLOBAIS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #f8f6f0;
    color: #1a1a2e;
}

[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #e8e0d0 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #252545 !important;
    border-color: #3a3a5c !important;
    color: #e8e0d0 !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #252545 !important;
    border-color: #3a3a5c !important;
}
[data-testid="stSidebar"] hr { border-color: #3a3a5c; }

.kpi-card {
    background: #1a1a2e;
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.6s ease forwards;
    opacity: 0;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c8a96e, #e8c97e);
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8888aa;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #c8a96e;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #6666aa;
    margin-top: 6px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0 0 4px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #c8a96e;
    display: inline-block;
}
.section-sub {
    font-size: 0.82rem;
    color: #666688;
    margin-bottom: 24px;
    font-weight: 400;
}

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 55%, #0f3460 100%);
    border-radius: 20px;
    padding: 56px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.9s ease;
}
.hero::after {
    content: '🇧🇷';
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 9rem;
    opacity: 0.1;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    color: #f0ece0;
    line-height: 1.1;
    margin-bottom: 16px;
}
.hero-desc {
    font-size: 1rem;
    color: #9090b8;
    max-width: 560px;
    line-height: 1.8;
}

.about-section {
    background: white;
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 20px;
    border-left: 4px solid #c8a96e;
    animation: slideUp 0.5s ease forwards;
    opacity: 0;
}
.about-section h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #1a1a2e;
    margin-bottom: 12px;
}
.about-section p {
    font-size: 0.9rem;
    color: #444466;
    line-height: 1.8;
}

.methodology-step {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}
.step-num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    color: #c8a96e;
    line-height: 1;
    min-width: 40px;
}
.step-content h4 { color: #1a1a2e; margin-bottom: 4px; font-size: 0.9rem; }
.step-content p  { color: #666688; font-size: 0.82rem; line-height: 1.6; }

.gold-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c8a96e, transparent);
    margin: 32px 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.delay-1 { animation-delay: 0.05s; }
.delay-2 { animation-delay: 0.15s; }
.delay-3 { animation-delay: 0.25s; }
.delay-4 { animation-delay: 0.35s; }
.delay-5 { animation-delay: 0.45s; }

div.block-container { padding-top: 2rem; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 8px 8px 0 0;
    border: 1px solid #e0d8c8;
    color: #3a3a5c;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: #1a1a2e !important;
    color: #c8a96e !important;
    border-color: #1a1a2e !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# DADOS
# ══════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    dados = {
        "Estado": [
            "Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará",
            "Distrito Federal","Espírito Santo","Goiás","Maranhão",
            "Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará",
            "Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro",
            "Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima",
            "Santa Catarina","São Paulo","Sergipe","Tocantins"
        ],
        "Sigla": [
            "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
            "MT","MS","MG","PA","PB","PR","PE","PI","RJ",
            "RN","RS","RO","RR","SC","SP","SE","TO"
        ],
        "Regiao": [
            "Norte","Nordeste","Norte","Norte","Nordeste","Nordeste",
            "Centro-Oeste","Sudeste","Centro-Oeste","Nordeste",
            "Centro-Oeste","Centro-Oeste","Sudeste","Norte",
            "Nordeste","Sul","Nordeste","Nordeste","Sudeste",
            "Nordeste","Sul","Norte","Norte","Sul","Sudeste","Nordeste","Norte"
        ],
        "Vereadores": [
            855,2890,680,3100,11200,5760,24,1890,4620,4870,
            3200,2510,19800,5120,3200,7640,5520,3010,5040,
            2780,6380,1870,630,4560,25100,1520,1890
        ],
        "Prefeitos_Alinhados_pct": [
            68,72,55,61,59,64,100,70,66,71,
            58,62,67,63,69,72,65,70,58,
            66,71,60,57,74,63,68,65
        ],
        "Indice_Gov": [
            62,55,58,60,67,63,81,72,70,53,
            65,68,74,57,61,76,64,56,59,
            62,73,61,57,79,78,60,63
        ],
        "Partido_Gov": [
            "PT","União Brasil","PDT","PL","PT","PT","PL","PL","PSD","PSD",
            "PL","PSD","PSD","União Brasil","PT","PL","PT","PT","PL",
            "PSD","PL","PL","PL","PL","PSD","PSD","PSD"
        ],
        "Eleitorado_M": [
            0.6,2.4,0.6,2.5,12.1,6.8,2.2,3.2,5.1,4.5,
            2.6,2.1,16.3,6.3,3.1,9.2,7.1,2.5,13.2,
            2.5,8.8,1.3,0.4,5.9,35.0,1.7,1.2
        ],
        "IDH": [
            0.663,0.683,0.708,0.674,0.660,0.682,0.824,0.740,0.735,0.639,
            0.725,0.729,0.731,0.646,0.683,0.749,0.673,0.655,0.711,
            0.684,0.746,0.690,0.707,0.774,0.783,0.665,0.699
        ],
        "PIB_per_capita": [
            18200,14800,22100,20400,17600,18900,85300,38700,32100,13200,
            42800,36500,27800,19600,16400,40200,19800,14600,32100,
            19200,42300,24600,28800,45100,52300,18100,22400
        ],
        "Municipios": [
            22,102,16,62,417,184,1,78,246,217,
            141,79,853,144,223,399,185,224,92,
            167,497,52,15,295,645,75,139
        ],
    }
    return pd.DataFrame(dados)


@st.cache_data(ttl=3600)
def load_geojson():
    import requests
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    try:
        r = requests.get(url, timeout=12)
        return r.json()
    except Exception:
        return None


df = load_data()
geojson = load_geojson()

CORES_PARTIDO = {
    "PT":           "#e53935",
    "PL":           "#1565c0",
    "PSD":          "#2e7d32",
    "União Brasil": "#e65100",
    "PDT":          "#6a1b9a",
}
CORES_REGIAO = {
    "Norte":        "#0077b6",
    "Nordeste":     "#e07c00",
    "Centro-Oeste": "#388e3c",
    "Sudeste":      "#7b1fa2",
    "Sul":          "#c62828",
}

PLOTLY_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="#fafaf7",
    font=dict(family="DM Sans, sans-serif", color="#1a1a2e"),
    margin=dict(l=12, r=12, t=40, b=12),
)


# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:24px 0 20px;'>
        <div style='font-family:"Playfair Display",serif; font-size:1.45rem;
                    font-weight:900; color:#c8a96e; letter-spacing:0.02em;'>
            🗳️ Brasil Político
        </div>
        <div style='font-size:0.68rem; letter-spacing:0.18em; text-transform:uppercase;
                    color:#6666aa; margin-top:6px;'>
            Dashboard Eleitoral · 2024
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#3a3a5c; margin:0 0 20px;'>", unsafe_allow_html=True)

    pagina = st.selectbox(
        "Página",
        ["🏠  Visão Geral", "🗺️  Mapa Interativo", "📊  Análises", "📋  Dados Completos", "ℹ️  Sobre o Projeto"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#3a3a5c; margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.7rem; color:#8888aa; letter-spacing:0.1em;
                text-transform:uppercase; margin-bottom:10px;'>
        Filtros Globais
    </div>
    """, unsafe_allow_html=True)

    regioes_disp = sorted(df["Regiao"].unique())
    regioes_sel = st.multiselect("Região", regioes_disp, default=regioes_disp)

    partidos_disp = sorted(df["Partido_Gov"].unique())
    partidos_sel = st.multiselect("Partido do Governador", partidos_disp, default=partidos_disp)

    st.markdown("<hr style='border-color:#3a3a5c; margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.68rem; color:#555577; line-height:1.9; text-align:center;'>
        Fontes: TSE · IBGE · PNUD · BCB<br>
        <span style='color:#444466;'>⚠️ Dados ilustrativos</span>
    </div>
    """, unsafe_allow_html=True)

df_f = df[df["Regiao"].isin(regioes_sel) & df["Partido_Gov"].isin(partidos_sel)]


def chart_title(title, subtitle=""):
    sub_html = f'<br><span style="font-size:0.75rem;color:#888899;">{subtitle}</span>' if subtitle else ""
    st.markdown(f"""
    <div style='margin-bottom:8px;'>
        <span style='font-family:"Playfair Display",serif; font-size:1.05rem;
                     font-weight:700; color:#1a1a2e;'>{title}</span>{sub_html}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════
if "Visão Geral" in pagina:

    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Análise Político-Eleitoral · 2024</div>
        <div class="hero-title">Brasil Político</div>
        <div class="hero-desc">
            Um panorama abrangente do cenário político brasileiro: distribuição de poder,
            índices de desenvolvimento e governabilidade por estado e região.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        ("Estados", f"{len(df_f)}", "selecionados", "delay-1"),
        ("Eleitorado", f"{df_f['Eleitorado_M'].sum():.1f}M", "eleitores registrados", "delay-2"),
        ("Municípios", f"{df_f['Municipios'].sum():,}", "no total", "delay-3"),
        ("IDH Médio", f"{df_f['IDH'].mean():.3f}", "média ponderada", "delay-4"),
        ("Governabilidade", f"{df_f['Indice_Gov'].mean():.0f}", "pontos / 100", "delay-5"),
    ]
    for col, (lbl, val, sub, delay) in zip([c1, c2, c3, c4, c5], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card {delay}">
                <div class="kpi-label">{lbl}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    col_m, col_p = st.columns([3, 2])

    with col_m:
        chart_title("Governabilidade por Estado", "Índice composto 0–100 · quanto maior, mais estável")
        if geojson:
            fig = px.choropleth(
                df_f, geojson=geojson, locations="Sigla",
                featureidkey="properties.sigla",
                color="Indice_Gov",
                color_continuous_scale=[[0,"#e8e0d0"],[0.5,"#c8a96e"],[1,"#1a1a2e"]],
                hover_name="Estado",
                hover_data={"Sigla":False,"Partido_Gov":True,"IDH":":.3f","Indice_Gov":True},
                labels={"Indice_Gov":"Gov.","Partido_Gov":"Partido"},
            )
            fig.update_geos(fitbounds="locations", visible=False, bgcolor="white")
            fig.update_layout(**PLOTLY_BASE, height=400,
                coloraxis_colorbar=dict(title="Gov.", tickfont=dict(size=11), len=0.6, thickness=14))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("GeoJSON não pôde ser carregado. Verifique a conexão.")

    with col_p:
        chart_title("Governadores por Partido", "Distribuição dos estados filtrados")
        contagem = df_f["Partido_Gov"].value_counts().reset_index()
        contagem.columns = ["Partido","Estados"]
        cores = [CORES_PARTIDO.get(p,"#aaaacc") for p in contagem["Partido"]]
        fig2 = go.Figure(go.Pie(
            labels=contagem["Partido"], values=contagem["Estados"],
            marker=dict(colors=cores, line=dict(color="white", width=2)),
            textinfo="label+percent", hole=0.5,
            textfont=dict(size=12, family="DM Sans"),
            hovertemplate="<b>%{label}</b><br>%{value} estado(s) · %{percent}<extra></extra>",
        ))
        fig2.update_layout(**PLOTLY_BASE, height=400,
            annotations=[dict(text="<b>Gov.</b>", x=0.5, y=0.5, showarrow=False,
                              font=dict(size=14, color="#888899"))],
            legend=dict(orientation="v", font=dict(size=11)),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    chart_title("Eleitorado por Região", "Total em milhões de eleitores registrados")
    reg = df_f.groupby("Regiao")["Eleitorado_M"].sum().reset_index().sort_values("Eleitorado_M", ascending=False)
    cores_r = [CORES_REGIAO.get(r,"#aaa") for r in reg["Regiao"]]
    fig3 = go.Figure(go.Bar(
        x=reg["Regiao"], y=reg["Eleitorado_M"],
        marker=dict(color=cores_r, line=dict(width=0)),
        text=reg["Eleitorado_M"].apply(lambda v: f"{v:.1f}M"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{y:.1f}M eleitores<extra></extra>",
    ))
    fig3.update_layout(**PLOTLY_BASE, height=320,
        yaxis=dict(title="Eleitorado (milhões)", gridcolor="#ede8dc"))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════
# PÁGINA 2 — MAPA INTERATIVO
# ══════════════════════════════════════════════════════════
elif "Mapa" in pagina:

    st.markdown("""
    <p class='section-title'>Mapa Interativo do Brasil</p>
    <p class='section-sub'>Selecione a métrica e explore o território nacional</p>
    """, unsafe_allow_html=True)

    METRICAS = {
        "Indice_Gov":    "Índice de Governabilidade",
        "IDH":           "IDH (PNUD)",
        "Eleitorado_M":  "Eleitorado (milhões)",
        "PIB_per_capita":"PIB per Capita (R$)",
        "Municipios":    "Nº de Municípios",
        "Vereadores":    "Nº de Vereadores",
    }

    col_ctrl1, col_ctrl2 = st.columns([2, 2])
    with col_ctrl1:
        metrica = st.selectbox("Métrica exibida no mapa", list(METRICAS.keys()),
                               format_func=lambda x: METRICAS[x])
    with col_ctrl2:
        paleta_nome = st.selectbox("Paleta de cores", [
            "Dourado · padrão", "Azul Naval", "Verde Floresta", "Vermelho", "Roxo"
        ])

    paleta_map = {
        "Dourado · padrão": [[0,"#f0ece0"],[0.5,"#c8a96e"],[1,"#1a1a2e"]],
        "Azul Naval":       [[0,"#e8f4f8"],[0.5,"#4a90d9"],[1,"#0d2b6e"]],
        "Verde Floresta":   [[0,"#f0f7f0"],[0.5,"#5aaa6a"],[1,"#1a4a2e"]],
        "Vermelho":         [[0,"#fff0f0"],[0.5,"#e05a5a"],[1,"#6e1a1a"]],
        "Roxo":             [[0,"#f5f0ff"],[0.5,"#9a6acd"],[1,"#3a1a6e"]],
    }

    if geojson:
        fig_mapa = px.choropleth(
            df_f, geojson=geojson, locations="Sigla",
            featureidkey="properties.sigla",
            color=metrica,
            color_continuous_scale=paleta_map[paleta_nome],
            hover_name="Estado",
            hover_data={
                "Sigla":False,"Regiao":True,"Partido_Gov":True,
                "IDH":":.3f","Eleitorado_M":":.1f",
                "PIB_per_capita":":,.0f","Indice_Gov":True,
            },
            labels={
                "Regiao":"Região","Partido_Gov":"Partido","IDH":"IDH",
                "Eleitorado_M":"Eleitorado (M)","PIB_per_capita":"PIB/cap (R$)",
                "Indice_Gov":"Gov.", metrica: METRICAS[metrica],
            },
        )
        fig_mapa.update_geos(fitbounds="locations", visible=False, bgcolor="#f8f6f0")
        fig_mapa.update_layout(**PLOTLY_BASE, height=560, paper_bgcolor="#f8f6f0",
            coloraxis_colorbar=dict(
                title=METRICAS[metrica], tickfont=dict(size=11),
                len=0.65, thickness=14,
            ),
        )
        st.plotly_chart(fig_mapa, use_container_width=True)

        st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
        chart_title(f"Top 10 — {METRICAS[metrica]}", "Cores por partido do governador")
        top10 = df_f.nlargest(10, metrica)[["Estado","Partido_Gov", metrica]].copy()
        cores_bar = [CORES_PARTIDO.get(p,"#aaa") for p in top10["Partido_Gov"]]

        fig_rank = go.Figure(go.Bar(
            y=top10["Estado"], x=top10[metrica],
            orientation="h",
            marker=dict(color=cores_bar, line=dict(width=0)),
            text=top10[metrica].apply(
                lambda v: f"R$ {v:,.0f}" if metrica == "PIB_per_capita"
                else (f"{v:.3f}" if metrica == "IDH" else f"{v:,.0f}")
            ),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x}<extra></extra>",
        ))
        fig_rank.update_layout(**PLOTLY_BASE, height=340,
            yaxis=dict(autorange="reversed", gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#ede8dc"),
        )
        st.plotly_chart(fig_rank, use_container_width=True)
    else:
        st.error("Não foi possível carregar o GeoJSON. Verifique a conexão com a internet.")


# ══════════════════════════════════════════════════════════
# PÁGINA 3 — ANÁLISES
# ══════════════════════════════════════════════════════════
elif "Análises" in pagina:

    st.markdown("""
    <p class='section-title'>Análises Políticas</p>
    <p class='section-sub'>Cruzamentos e correlações entre variáveis socioeconômicas e políticas</p>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🔵  IDH × Governabilidade",
        "🟠  Comparativo Regional",
        "🟢  Análise Partidária",
    ])

    with tab1:
        chart_title("IDH × Índice de Governabilidade",
                    "Tamanho da bolha = eleitorado · cor = partido · linha = tendência")
        fig_sc = px.scatter(
            df_f, x="IDH", y="Indice_Gov",
            color="Partido_Gov", size="Eleitorado_M",
            text="Sigla",
            color_discrete_map=CORES_PARTIDO,
            hover_name="Estado",
            hover_data={"Sigla":False,"Regiao":True,"PIB_per_capita":":,.0f"},
            labels={
                "IDH":"IDH (PNUD)", "Indice_Gov":"Índice de Governabilidade",
                "Partido_Gov":"Partido","Eleitorado_M":"Eleitorado (M)",
                "PIB_per_capita":"PIB/cap (R$)",
            },
            trendline="ols",
            trendline_scope="overall",
            trendline_color_override="#c8a96e",
        )
        fig_sc.update_traces(
            selector=dict(mode="markers+text"),
            textposition="top center",
            textfont=dict(size=10, family="DM Mono"),
            marker=dict(opacity=0.85, line=dict(width=1.5, color="white")),
        )
        fig_sc.update_layout(**PLOTLY_BASE, height=480,
            xaxis=dict(gridcolor="#ede8dc"),
            yaxis=dict(gridcolor="#ede8dc"),
            legend=dict(bgcolor="white", bordercolor="#e0d8c8", borderwidth=1),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

        corr = df_f["IDH"].corr(df_f["Indice_Gov"])
        nivel = "moderada positiva" if corr > 0.4 else ("fraca positiva" if corr > 0 else "fraca negativa")
        st.info(f"📐 **Correlação de Pearson:** {corr:.3f} — {nivel} entre IDH e Governabilidade nos estados selecionados.")

    with tab2:
        chart_title("Radar por Região", "Comparação multidimensional · escalas normalizadas")
        reg_stats = df_f.groupby("Regiao").agg(
            IDH_medio=("IDH","mean"),
            Gov_medio=("Indice_Gov","mean"),
            PIB_medio=("PIB_per_capita","mean"),
            Eleitorado=("Eleitorado_M","sum"),
        ).reset_index()

        cats = ["IDH (×10)", "Governabilidade (÷10)", "PIB (÷10k)"]
        fig_radar = go.Figure()
        for _, row in reg_stats.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["IDH_medio"]*10, row["Gov_medio"]/10, row["PIB_medio"]/10000],
                theta=cats, fill="toself", name=row["Regiao"],
                line=dict(color=CORES_REGIAO.get(row["Regiao"],"#aaa"), width=2.5),
                fillcolor=CORES_REGIAO.get(row["Regiao"],"#aaa"),
                opacity=0.25,
            ))
        fig_radar.update_layout(**PLOTLY_BASE, height=440,
            polar=dict(
                bgcolor="#fafaf7",
                radialaxis=dict(visible=True, gridcolor="#e0d8c8"),
                angularaxis=dict(gridcolor="#e0d8c8"),
            ),
            legend=dict(bgcolor="white", bordercolor="#e0d8c8", borderwidth=1),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            chart_title("PIB per Capita Médio por Região")
            fig_pib = px.bar(
                reg_stats.sort_values("PIB_medio"),
                x="PIB_medio", y="Regiao", orientation="h",
                color="Regiao", color_discrete_map=CORES_REGIAO,
                text="PIB_medio",
                labels={"PIB_medio":"PIB per Capita (R$)","Regiao":""},
            )
            fig_pib.update_traces(texttemplate="R$ %{text:,.0f}", textposition="outside")
            fig_pib.update_layout(**PLOTLY_BASE, height=300, showlegend=False,
                xaxis=dict(gridcolor="#ede8dc"))
            st.plotly_chart(fig_pib, use_container_width=True)

        with col_b:
            chart_title("IDH Médio por Região")
            fig_idh = px.bar(
                reg_stats.sort_values("IDH_medio"),
                x="IDH_medio", y="Regiao", orientation="h",
                color="Regiao", color_discrete_map=CORES_REGIAO,
                text="IDH_medio",
                labels={"IDH_medio":"IDH","Regiao":""},
            )
            fig_idh.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig_idh.update_layout(**PLOTLY_BASE, height=300, showlegend=False,
                xaxis=dict(gridcolor="#ede8dc", range=[0.6, 0.87]))
            st.plotly_chart(fig_idh, use_container_width=True)

    with tab3:
        chart_title("IDH e Governabilidade por Partido", "Médias dos estados governados por cada partido")
        part_stats = df_f.groupby("Partido_Gov").agg(
            Estados=("Estado","count"),
            IDH=("IDH","mean"),
            Gov=("Indice_Gov","mean"),
            PIB=("PIB_per_capita","mean"),
            Eleitorado=("Eleitorado_M","sum"),
        ).reset_index().sort_values("Eleitorado", ascending=False)

        fig_part = px.bar(
            part_stats, x="Partido_Gov", y=["IDH","Gov"],
            barmode="group",
            color_discrete_sequence=["#c8a96e","#1a1a2e"],
            labels={"value":"Valor","variable":"Indicador","Partido_Gov":"Partido"},
        )
        fig_part.update_layout(**PLOTLY_BASE, height=360,
            yaxis=dict(gridcolor="#ede8dc"),
            legend=dict(bgcolor="white"),
        )
        st.plotly_chart(fig_part, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        chart_title("Resumo por Partido")
        part_fmt = part_stats.copy()
        part_fmt.columns = ["Partido","Estados","IDH Médio","Gov. Médio","PIB Médio","Eleitorado (M)"]
        st.dataframe(
            part_fmt.style
                .format({"IDH Médio":"{:.3f}","Gov. Médio":"{:.1f}",
                         "PIB Médio":"R$ {:,.0f}","Eleitorado (M)":"{:.1f}"})
                .background_gradient(subset=["IDH Médio"], cmap="YlOrBr")
                .background_gradient(subset=["Gov. Médio"], cmap="Greens"),
            use_container_width=True, height=260,
        )


# ══════════════════════════════════════════════════════════
# PÁGINA 4 — DADOS COMPLETOS
# ══════════════════════════════════════════════════════════
elif "Dados" in pagina:

    st.markdown("""
    <p class='section-title'>Dados Completos</p>
    <p class='section-sub'>Tabela detalhada com todos os indicadores por estado</p>
    """, unsafe_allow_html=True)

    col_ord, col_dir = st.columns([2, 1])
    with col_ord:
        ordem = st.selectbox("Ordenar por", [
            "Estado","IDH","Indice_Gov","PIB_per_capita","Eleitorado_M","Municipios"
        ])
    with col_dir:
        crescente = st.radio("Direção", ["↑ Crescente","↓ Decrescente"], horizontal=True) == "↑ Crescente"

    df_exib = df_f.sort_values(ordem, ascending=crescente)[[
        "Estado","Sigla","Regiao","Partido_Gov","IDH",
        "Indice_Gov","Eleitorado_M","PIB_per_capita","Municipios","Vereadores"
    ]].copy()
    df_exib.columns = [
        "Estado","UF","Região","Partido Gov.","IDH",
        "Gov. (pts)","Eleitorado (M)","PIB per Capita","Municípios","Vereadores"
    ]

    st.dataframe(
        df_exib.style
            .background_gradient(subset=["IDH"], cmap="YlOrBr")
            .background_gradient(subset=["Gov. (pts)"], cmap="Greens")
            .background_gradient(subset=["PIB per Capita"], cmap="Blues")
            .format({
                "IDH":"{:.3f}","Gov. (pts)":"{:.0f}",
                "Eleitorado (M)":"{:.1f}",
                "PIB per Capita":"R$ {:,.0f}",
                "Municípios":"{:,}","Vereadores":"{:,}",
            }),
        use_container_width=True, height=540,
    )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv = df_exib.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Exportar como CSV", csv,
                           "brasil_politico.csv", "text/csv",
                           use_container_width=True)
    with col_dl2:
        st.info(f"📌 **{len(df_exib)}** estados exibidos com os filtros atuais.")


# ══════════════════════════════════════════════════════════
# PÁGINA 5 — SOBRE O PROJETO
# ══════════════════════════════════════════════════════════
elif "Sobre" in pagina:

    st.markdown("""
    <p class='section-title'>Sobre o Projeto</p>
    <p class='section-sub'>Documentação, metodologia e fontes dos dados utilizados</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='about-section delay-1'>
        <h3>🎯 Objetivo</h3>
        <p>
            Este dashboard foi desenvolvido com o objetivo de oferecer uma visualização clara,
            interativa e acessível do panorama político-eleitoral brasileiro. Por meio de mapas,
            gráficos e análises comparativas, o projeto busca tornar dados públicos mais compreensíveis
            para pesquisadores, estudantes, jornalistas e cidadãos interessados em política.
        </p>
        <p style='margin-top:12px;'>
            O foco está na relação entre variáveis socioeconômicas — como IDH e PIB per capita —
            e indicadores de governabilidade política, permitindo identificar padrões regionais
            e tendências eleitorais ao longo do território nacional.
        </p>
    </div>

    <div class='about-section delay-2'>
        <h3>🔬 Metodologia</h3>
    """, unsafe_allow_html=True)

    etapas = [
        ("01", "Coleta de Dados",
         "Dados extraídos de fontes primárias oficiais: TSE, IBGE, PNUD Brasil e Banco Central do Brasil. "
         "Os dados foram coletados e consolidados para o período de referência 2022–2024."),
        ("02", "Normalização",
         "Variáveis de diferentes escalas foram normalizadas para permitir comparações justas entre "
         "estados com perfis populacionais muito distintos, como São Paulo e Roraima."),
        ("03", "Índice de Governabilidade",
         "Indicador composto calculado com base em alinhamento legislativo, coalizões municipais, "
         "aprovação orçamentária e histórico de vetos. Escala de 0 a 100."),
        ("04", "Visualização",
         "Construído com Streamlit e Plotly para máxima interatividade. O mapa coroplético utiliza "
         "dados geoespaciais em formato GeoJSON com coordenadas oficiais dos estados brasileiros."),
    ]
    for num, titulo, desc in etapas:
        st.markdown(f"""
        <div class='methodology-step'>
            <div class='step-num'>{num}</div>
            <div class='step-content'>
                <h4>{titulo}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='about-section delay-3'>
        <h3>📚 Fontes de Dados</h3>
        <p>Os dados utilizados neste projeto são provenientes de fontes públicas e oficiais:</p>
        <br>
    """, unsafe_allow_html=True)

    fontes = [
        ("🏛️", "TSE — Tribunal Superior Eleitoral",
         "Dados eleitorais: eleitorado, resultados, filiação partidária e composição de câmaras municipais.",
         "https://www.tse.jus.br/"),
        ("📊", "IBGE — Instituto Brasileiro de Geografia e Estatística",
         "Dados demográficos e territoriais: população, municípios, regiões e PIB per capita estadual.",
         "https://www.ibge.gov.br/"),
        ("🌍", "PNUD Brasil — Programa das Nações Unidas para o Desenvolvimento",
         "Índice de Desenvolvimento Humano (IDH) municipal e estadual — Atlas Brasil.",
         "https://www.undp.org/pt/brazil"),
        ("💰", "BCB — Banco Central do Brasil",
         "Dados macroeconômicos regionais e indicadores fiscais dos estados.",
         "https://www.bcb.gov.br/"),
        ("🗺️", "Code for America · GeoJSON",
         "Geometrias geoespaciais dos estados brasileiros em formato GeoJSON para o mapa coroplético.",
         "https://github.com/codeforamerica/click_that_hood"),
    ]
    for icone, nome, desc, url in fontes:
        st.markdown(f"""
        <div style='display:flex; gap:16px; align-items:flex-start; margin-bottom:16px;
                    padding:16px; background:#f8f6f0; border-radius:10px;'>
            <div style='font-size:1.8rem; line-height:1; flex-shrink:0;'>{icone}</div>
            <div>
                <div style='font-weight:600; color:#1a1a2e; font-size:0.9rem;'>{nome}</div>
                <div style='color:#666688; font-size:0.82rem; line-height:1.7; margin:4px 0 6px;'>{desc}</div>
                <a href='{url}' target='_blank'
                   style='color:#c8a96e; font-size:0.78rem; text-decoration:none;
                          font-family:"DM Mono",monospace;'>{url} ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='about-section delay-4' style='border-left-color:#e07c00;'>
        <h3>⚠️ Aviso Importante</h3>
        <p>
            Os dados apresentados neste dashboard são <strong>ilustrativos e têm finalidade
            exclusivamente educacional e demonstrativa</strong>. O Índice de Governabilidade é
            um indicador fictício criado para fins de demonstração da plataforma.
        </p>
        <p style='margin-top:10px;'>
            Os valores de eleitorado, IDH e PIB per capita são aproximações baseadas em dados
            reais do período 2022–2024, mas podem divergir dos valores oficiais mais recentes.
            Para análises oficiais ou tomada de decisão, consulte diretamente as fontes primárias.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-family:\"Playfair Display\",serif; font-size:1.1rem; font-weight:700; color:#1a1a2e;'>Stack Tecnológico</p>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    stack = [
        ("🐍","Python 3.11","Linguagem base"),
        ("⚡","Streamlit","Framework web"),
        ("📈","Plotly","Visualizações"),
        ("🐼","Pandas","Dados tabulares"),
        ("🗺️","GeoJSON","Geoespacial"),
    ]
    for col, (icon, nome, desc) in zip([c1,c2,c3,c4,c5], stack):
        with col:
            st.markdown(f"""
            <div style='text-align:center; background:white; border-radius:12px;
                        padding:20px 12px; border:1px solid #e0d8c8; transition:all 0.2s;'>
                <div style='font-size:2rem;'>{icon}</div>
                <div style='font-weight:600; color:#1a1a2e; font-size:0.85rem; margin-top:8px;'>{nome}</div>
                <div style='color:#888899; font-size:0.72rem; margin-top:4px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; color:#aaaacc; font-size:0.75rem; padding:28px 0 8px;
                border-top:1px solid #e0d8c8; margin-top:36px;'>
        Brasil Político Dashboard · 2024 · Desenvolvido com ❤️ usando Streamlit &amp; Plotly
    </div>
    """, unsafe_allow_html=True)
