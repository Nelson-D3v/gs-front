import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

STATES = ["Amazonas", "Pará", "Mato Grosso", "Rondônia", "Tocantins", "Bahia", "Minas Gerais", "Goiás"]
BIOMES = ["Amazônia", "Cerrado", "Caatinga", "Mata Atlântica", "Pantanal"]


@st.cache_data(ttl=300)
def fetch_fire_data(start_date: str, end_date: str) -> pd.DataFrame:
    np.random.seed(42)
    days = pd.date_range(start=start_date, end=end_date, freq="D")
    records = []
    for day in days:
        n = np.random.randint(20, 120)
        for _ in range(n):
            state = np.random.choice(STATES, p=[0.25, 0.20, 0.15, 0.10, 0.08, 0.08, 0.07, 0.07])
            biome = np.random.choice(BIOMES)
            risk = np.random.choice(["Baixo", "Moderado", "Alto", "Crítico"],
                                    p=[0.2, 0.3, 0.3, 0.2])
            records.append({
                "date": day,
                "state": state,
                "biome": biome,
                "lat": np.random.uniform(-15, -3),
                "lon": np.random.uniform(-65, -45),
                "frp": round(np.random.exponential(50), 1),  # Fire Radiative Power (MW)
                "risk_level": risk,
                "area_ha": round(np.random.exponential(200), 1),
            })
    return pd.DataFrame(records)


@st.cache_data(ttl=300)
def fetch_climate_data(start_date: str, end_date: str) -> pd.DataFrame:
    np.random.seed(7)
    days = pd.date_range(start=start_date, end=end_date, freq="D")
    records = []
    for day in days:
        for state in STATES:
            records.append({
                "date": day,
                "state": state,
                "temperature": round(np.random.uniform(25, 42), 1),
                "humidity": round(np.random.uniform(10, 70), 1),
                "wind_speed": round(np.random.uniform(0, 30), 1),
                "precipitation": round(max(0, np.random.normal(2, 5)), 1),
            })
    return pd.DataFrame(records)
