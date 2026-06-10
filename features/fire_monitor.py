import streamlit as st
from ui.charts import scatter_map, donut_risk
from ui.components import metric_card, loading_spinner
from pipelines.fire_pipeline import aggregate_by_risk

RISK_COLORS = {"Baixo": "#2ecc71", "Moderado": "#f39c12", "Alto": "#e67e22", "Crítico": "#e74c3c"}


def render_fire_monitor(fire_df, climate_df):
    st.markdown("## Mapa de Focos & Risco")

    with loading_spinner("Carregando dados de localização..."):
        risk_df = aggregate_by_risk(fire_df)

    col1, col2 = st.columns([2, 1])
    with col1:
        if not fire_df.empty:
            st.plotly_chart(scatter_map(fire_df), use_container_width=True)
        else:
            st.info("Nenhum foco encontrado para os filtros selecionados.")
    with col2:
        st.plotly_chart(donut_risk(risk_df), use_container_width=True)
        st.divider()
        st.markdown("**Resumo por Risco**")
        for _, row in risk_df.iterrows():
            color = RISK_COLORS.get(row["risk_level"], "#aaa")
            metric_card(row["risk_level"], f"{row['count']:,} focos", color=color)
