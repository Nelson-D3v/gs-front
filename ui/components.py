import streamlit as st

RISK_COLORS = {
    "Baixo": "#2ecc71",
    "Moderado": "#f39c12",
    "Alto": "#e67e22",
    "Crítico": "#e74c3c",
}

RISK_ICONS = {
    "Baixo": "🟢",
    "Moderado": "🟡",
    "Alto": "🟠",
    "Crítico": "🔴",
}


def metric_card(label: str, value, delta=None, color: str = "#e74c3c"):
    delta_html = f"<p style='margin:0;font-size:12px;color:#aaa;'>{delta}</p>" if delta else ""
    st.markdown(
        f"""
        <div style='background:#1e1e2e;border-left:4px solid {color};
                    padding:16px 20px;border-radius:8px;margin-bottom:8px;'>
            <p style='margin:0;font-size:13px;color:#aaa;'>{label}</p>
            <p style='margin:4px 0 0;font-size:28px;font-weight:700;color:{color};'>{value}</p>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(risk: str):
    color = RISK_COLORS.get(risk, "#aaa")
    icon = RISK_ICONS.get(risk, "⚪")
    st.markdown(
        f"<span style='background:{color};color:white;padding:3px 10px;"
        f"border-radius:12px;font-size:12px;font-weight:600;'>{icon} {risk}</span>",
        unsafe_allow_html=True,
    )


def alert_card(alert: dict, key_prefix: str):
    """Human-in-the-loop: exibe alerta gerado pelo sistema para aprovação do usuário."""
    color = RISK_COLORS.get(alert["risk"], "#e74c3c")
    with st.container():
        st.markdown(
            f"""
            <div style='border:1px solid {color};border-radius:10px;padding:16px;
                        background:#1e1e2e;margin-bottom:12px;'>
                <b style='color:{color};font-size:15px;'>
                    {RISK_ICONS.get(alert["risk"],"🔴")} Alerta {alert["risk"]} — {alert["state"]}
                </b>
                <p style='margin:6px 0;color:#ddd;font-size:13px;'>
                    {alert["message"]}
                </p>
                <p style='margin:0;color:#888;font-size:11px;'>
                    Focos detectados: <b>{alert["focos"]}</b> |
                    Área estimada: <b>{alert["area"]:.0f} ha</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        approved = col1.button("✅ Aprovar envio", key=f"{key_prefix}_approve", use_container_width=True)
        dismissed = col2.button("❌ Descartar", key=f"{key_prefix}_dismiss", use_container_width=True)
        return approved, dismissed


def loading_spinner(text: str = "Carregando dados satelitais..."):
    return st.spinner(text)
