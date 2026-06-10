import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from models.risk_predictor import predict_risk, get_feature_importance
from ui.components import metric_card, loading_spinner, risk_badge

RISK_COLOR_MAP = {"Baixo": "#2ecc71", "Moderado": "#f39c12", "Alto": "#e67e22", "Crítico": "#e74c3c"}


def render_ai_forecast(fire_df, climate_df):
    st.markdown("## Previsão de Risco com IA")
    st.markdown(
        "> Modelo preditivo baseado em **regressão linear com features climáticas e históricas**. "
        "Prevê o nível de risco e focos estimados por estado para os próximos dias."
    )

    col_h, col_s = st.columns([1, 3])
    with col_h:
        horizon = st.slider("Horizonte de previsão (dias)", min_value=3, max_value=14, value=7)
    with col_s:
        selected_states = st.multiselect(
            "Estados para previsão",
            options=["Amazonas", "Pará", "Mato Grosso", "Rondônia", "Tocantins", "Bahia", "Minas Gerais", "Goiás"],
            default=["Amazonas", "Pará", "Mato Grosso"],
        )

    if fire_df.empty:
        st.warning("Selecione mais dados nos filtros para gerar previsão.")
        return

    with loading_spinner("Executando modelo preditivo..."):
        cache_key = f"{len(fire_df)}_{fire_df['date'].max()}_{horizon}"
        forecast_df = predict_risk(cache_key, fire_df, climate_df, horizon)

    forecast_filtered = forecast_df[forecast_df["state"].isin(selected_states)] if selected_states else forecast_df

    # KPIs
    avg_score = forecast_filtered["risk_score"].mean()
    max_risk_row = forecast_filtered.loc[forecast_filtered["risk_score"].idxmax()]
    avg_focos = int(forecast_filtered["focos_pred"].mean())
    avg_conf = forecast_filtered["confidence"].mean()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        color = _score_to_color(avg_score)
        metric_card("Score Médio de Risco", f"{avg_score:.2f}/1.00", color=color)
    with k2:
        metric_card("Estado mais crítico", max_risk_row["state"], color="#e74c3c")
    with k3:
        metric_card("Focos Previstos/dia", f"~{avg_focos}", color="#e67e22")
    with k4:
        metric_card("Confiança média", f"{avg_conf:.0%}", color="#3498db")

    st.divider()

    tab_a, tab_b, tab_c = st.tabs(["📈 Evolução do Risco", "🗂️ Tabela de Previsão", "🔬 Importância das Features"])

    with tab_a:
        fig = px.line(
            forecast_filtered, x="date", y="risk_score", color="state",
            title=f"Score de Risco Previsto — próximos {horizon} dias",
            labels={"date": "Data", "risk_score": "Score de Risco (0–1)", "state": "Estado"},
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig.add_hline(y=0.75, line_dash="dot", line_color="#e74c3c", annotation_text="Crítico")
        fig.add_hline(y=0.50, line_dash="dot", line_color="#e67e22", annotation_text="Alto")
        fig.add_hline(y=0.25, line_dash="dot", line_color="#f39c12", annotation_text="Moderado")
        fig.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Faixa de confiança (intervalo)
        fig2 = go.Figure()
        for state in selected_states:
            sdf = forecast_filtered[forecast_filtered["state"] == state].sort_values("date")
            margin = (1 - sdf["confidence"]) * 0.1
            fig2.add_trace(go.Scatter(
                x=list(sdf["date"]) + list(sdf["date"])[::-1],
                y=list((sdf["risk_score"] + margin).clip(0, 1)) + list((sdf["risk_score"] - margin).clip(0, 1))[::-1],
                fill="toself", opacity=0.15, line_color="rgba(0,0,0,0)",
                name=f"{state} (IC 85%)",
            ))
            fig2.add_trace(go.Scatter(
                x=sdf["date"], y=sdf["risk_score"],
                mode="lines", name=state, line_width=2,
            ))
        fig2.update_layout(
            title="Score com Intervalo de Confiança (85%)",
            template="plotly_dark", paper_bgcolor="#0e1117",
            hovermode="x unified",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab_b:
        display = forecast_filtered[["date", "state", "risk_score", "risk_label", "focos_pred", "confidence"]].copy()
        display.columns = ["Data", "Estado", "Score", "Nível de Risco", "Focos Previstos", "Confiança"]
        display["Data"] = display["Data"].dt.strftime("%d/%m/%Y")
        display["Score"] = display["Score"].map("{:.3f}".format)
        display["Confiança"] = display["Confiança"].map("{:.0%}".format)
        st.dataframe(
            display.style.applymap(
                lambda v: f"color: {RISK_COLOR_MAP.get(v, 'white')}; font-weight: bold",
                subset=["Nível de Risco"],
            ),
            use_container_width=True,
            hide_index=True,
        )

    with tab_c:
        fi = get_feature_importance()
        fig3 = px.bar(
            fi, x="importance", y="feature", orientation="h",
            title="Importância das Features no Modelo",
            labels={"importance": "Peso", "feature": "Feature"},
            color="importance", color_continuous_scale="YlOrRd",
            template="plotly_dark",
            text="importance",
        )
        fig3.update_traces(texttemplate="%{text:.0%}", textposition="outside")
        fig3.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("**Descrição das Features**")
        for _, row in fi.iterrows():
            st.markdown(f"- **{row['feature']}** ({row['importance']:.0%}): {row['description']}")


def _score_to_color(score: float) -> str:
    if score >= 0.75:
        return "#e74c3c"
    if score >= 0.50:
        return "#e67e22"
    if score >= 0.25:
        return "#f39c12"
    return "#2ecc71"
