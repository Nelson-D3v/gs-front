import streamlit as st
from datetime import date, timedelta
from state import session_state as ss

STATES = ["Amazonas", "Pará", "Mato Grosso", "Rondônia", "Tocantins", "Bahia", "Minas Gerais", "Goiás"]
BIOMES = ["Amazônia", "Cerrado", "Caatinga", "Mata Atlântica", "Pantanal"]
RISKS = ["Baixo", "Moderado", "Alto", "Crítico"]


def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/fire.png", width=60)
        st.markdown("## 🔥 PyroWatch")
        st.caption("Sistema de Monitoramento de Queimadas")
        st.divider()

        st.markdown("### Filtros")

        start = st.date_input(
            "Data inicial",
            value=ss.get("start_date"),
            max_value=date.today(),
        )
        end = st.date_input(
            "Data final",
            value=ss.get("end_date"),
            min_value=start,
            max_value=date.today(),
        )

        states = st.multiselect(
            "Estados",
            options=STATES,
            default=ss.get("selected_states"),
        )

        biomes = st.multiselect(
            "Biomas",
            options=BIOMES,
            default=ss.get("selected_biomes"),
        )

        risks = st.multiselect(
            "Nível de Risco",
            options=RISKS,
            default=ss.get("selected_risks"),
        )

        if st.button("Aplicar Filtros", use_container_width=True, type="primary"):
            ss.set("start_date", start)
            ss.set("end_date", end)
            ss.set("selected_states", states if states else STATES)
            ss.set("selected_biomes", biomes if biomes else BIOMES)
            ss.set("selected_risks", risks if risks else RISKS)
            st.rerun()

        st.divider()
        st.caption("Dados simulados com base em padrões reais do INPE/NASA FIRMS.")
