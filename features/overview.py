import streamlit as st
from ui.components import metric_card, loading_spinner
from ui.charts import line_chart_focos, bar_chart_states, matplotlib_area_chart
from pipelines.fire_pipeline import aggregate_by_day, aggregate_by_state

RISK_COLORS = {"Baixo": "#2ecc71", "Moderado": "#f39c12", "Alto": "#e67e22", "Crítico": "#e74c3c"}


def render_overview(fire_df, climate_df):
    st.markdown("## Visão Geral")

    with loading_spinner("Processando dados satelitais..."):
        daily = aggregate_by_day(fire_df)
        by_state = aggregate_by_state(fire_df)

    total_focos = len(fire_df)
    area_total = fire_df["area_ha"].sum()
    estado_critico = by_state.iloc[0]["state"] if not by_state.empty else "-"
    risco_dominante = fire_df["risk_level"].value_counts().idxmax() if not fire_df.empty else "-"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total de Focos", f"{total_focos:,}", color=RISK_COLORS.get(risco_dominante, "#e74c3c"))
    with col2:
        metric_card("Área Estimada", f"{area_total:,.0f} ha", color="#e67e22")
    with col3:
        metric_card("Estado Crítico", estado_critico, color="#e74c3c")
    with col4:
        metric_card("Risco Dominante", risco_dominante, color=RISK_COLORS.get(risco_dominante, "#aaa"))

    st.divider()

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.plotly_chart(line_chart_focos(daily), use_container_width=True)
    with col_right:
        st.plotly_chart(bar_chart_states(by_state.head(6)), use_container_width=True)

    st.pyplot(matplotlib_area_chart(daily))
