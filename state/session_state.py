import streamlit as st
from datetime import date, timedelta


DEFAULTS = {
    "selected_states": ["Amazonas", "Pará", "Mato Grosso"],
    "selected_biomes": ["Amazônia", "Cerrado"],
    "selected_risks": ["Moderado", "Alto", "Crítico"],
    "start_date": date.today() - timedelta(days=30),
    "end_date": date.today(),
    "pending_alerts": [],
    "approved_alerts": [],
    "dismissed_alerts": [],
}


def init_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get(key):
    return st.session_state.get(key, DEFAULTS.get(key))


def set(key, value):
    st.session_state[key] = value
