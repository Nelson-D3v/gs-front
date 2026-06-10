import streamlit as st
from state import session_state as ss
from ui.sidebar import render_sidebar
from features.overview import render_overview
from features.fire_monitor import render_fire_monitor
from features.alerts import render_alerts
from features.ai_forecast import render_ai_forecast
from providers.fire_provider import fetch_fire_data, fetch_climate_data
from pipelines.fire_pipeline import filter_fire_data

st.set_page_config(
    page_title="PyroWatch",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0e1117; }
    [data-testid="stSidebar"] { background: #12121f; }
    h1, h2, h3, h4, h5 { color: #fff; }
    .stTabs [data-baseweb="tab"] { color: #aaa; }
    .stTabs [aria-selected="true"] { color: #e74c3c; border-bottom: 2px solid #e74c3c; }
    div[data-testid="metric-container"] { background: #1e1e2e; border-radius: 8px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

ss.init_state()

render_sidebar()

st.markdown(
    "<h1 style='color:#e74c3c;margin-bottom:0;'>🔥 PyroWatch</h1>"
    "<p style='color:#888;margin-top:4px;'>Plataforma de Monitoramento de Queimadas por Satélite</p>",
    unsafe_allow_html=True,
)
st.divider()

with st.spinner("Buscando dados satelitais e climáticos..."):
    raw_fire = fetch_fire_data(
        str(ss.get("start_date")),
        str(ss.get("end_date")),
    )
    raw_climate = fetch_climate_data(
        str(ss.get("start_date")),
        str(ss.get("end_date")),
    )

fire_df = filter_fire_data(
    raw_fire,
    states=ss.get("selected_states"),
    biomes=ss.get("selected_biomes"),
    risk_levels=ss.get("selected_risks"),
)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🗺️ Mapa & Risco", "🚨 Central de Alertas", "🤖 Previsão IA"])

with tab1:
    render_overview(fire_df, raw_climate)

with tab2:
    render_fire_monitor(fire_df, raw_climate)

with tab3:
    render_alerts(fire_df, raw_climate)

with tab4:
    render_ai_forecast(fire_df, raw_climate)
