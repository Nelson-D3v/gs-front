import streamlit as st
from ui.components import alert_card, loading_spinner, metric_card
from pipelines.fire_pipeline import aggregate_by_state
from state import session_state as ss


def _generate_alerts(fire_df):
    """Gera alertas automáticos com base nos focos críticos detectados."""
    if fire_df.empty:
        return []
    critical = fire_df[fire_df["risk_level"].isin(["Alto", "Crítico"])]
    by_state = aggregate_by_state(critical)
    alerts = []
    for i, row in by_state.head(4).iterrows():
        focos = row["total_focos"]
        area = row["area_total"]
        state = row["state"]
        risk = "Crítico" if focos > 200 else "Alto"
        alerts.append({
            "id": f"alert_{i}",
            "state": state,
            "risk": risk,
            "focos": focos,
            "area": area,
            "message": (
                f"Sistema detectou {focos} focos ativos em {state}. "
                f"Área estimada: {area:.0f} ha. "
                f"Recomenda-se emissão de alerta de {'evacuação preventiva' if risk == 'Crítico' else 'atenção'}."
            ),
        })
    return alerts


def render_alerts(fire_df, climate_df):
    st.markdown("## Central de Alertas")
    st.markdown(
        "> **Human-in-the-loop:** Os alertas abaixo foram gerados automaticamente pela análise de dados. "
        "Revise e **aprove** ou **descarte** cada um antes do envio."
    )

    with loading_spinner("Analisando focos críticos..."):
        generated = _generate_alerts(fire_df)

    if not generated:
        st.success("Nenhum alerta crítico detectado para os filtros atuais.")
        return

    approved = ss.get("approved_alerts")
    dismissed = ss.get("dismissed_alerts")

    pending = [a for a in generated if a["id"] not in approved and a["id"] not in dismissed]

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Alertas Gerados", len(generated), color="#e74c3c")
    with col2:
        metric_card("Aprovados", len(approved), color="#2ecc71")
    with col3:
        metric_card("Descartados", len(dismissed), color="#aaa")

    st.divider()

    if not pending:
        st.success("Todos os alertas foram revisados!")
    else:
        st.markdown(f"### {len(pending)} alerta(s) aguardando revisão")
        for alert in pending:
            do_approve, do_dismiss = alert_card(alert, key_prefix=alert["id"])
            if do_approve:
                ss.set("approved_alerts", approved + [alert["id"]])
                st.toast(f"Alerta de {alert['state']} APROVADO e enviado!", icon="✅")
                st.rerun()
            if do_dismiss:
                ss.set("dismissed_alerts", dismissed + [alert["id"]])
                st.toast(f"Alerta de {alert['state']} descartado.", icon="❌")
                st.rerun()

    if approved:
        st.divider()
        st.markdown("### Alertas Aprovados")
        for a in generated:
            if a["id"] in approved:
                st.success(f"✅ **{a['state']}** — {a['message']}")
