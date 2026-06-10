import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd

RISK_COLOR_MAP = {
    "Baixo": "#2ecc71",
    "Moderado": "#f39c12",
    "Alto": "#e67e22",
    "Crítico": "#e74c3c",
}


def line_chart_focos(df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        df, x="date", y="total_focos",
        title="Focos de Queimada por Dia",
        labels={"date": "Data", "total_focos": "Focos"},
        color_discrete_sequence=["#e74c3c"],
        template="plotly_dark",
    )
    fig.update_traces(line_width=2.5, mode="lines+markers", marker_size=4)
    fig.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        hovermode="x unified",
        margin=dict(t=40, b=20),
    )
    return fig


def bar_chart_states(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df, x="state", y="total_focos",
        title="Focos por Estado",
        labels={"state": "Estado", "total_focos": "Focos"},
        color="total_focos",
        color_continuous_scale="YlOrRd",
        template="plotly_dark",
    )
    fig.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        margin=dict(t=40, b=20),
        coloraxis_showscale=False,
    )
    return fig


def donut_risk(df: pd.DataFrame) -> go.Figure:
    colors = [RISK_COLOR_MAP.get(r, "#aaa") for r in df["risk_level"]]
    fig = go.Figure(go.Pie(
        labels=df["risk_level"],
        values=df["count"],
        hole=0.55,
        marker_colors=colors,
        textinfo="label+percent",
        hovertemplate="%{label}: %{value} focos<extra></extra>",
    ))
    fig.update_layout(
        title="Distribuição por Nível de Risco",
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        margin=dict(t=40, b=10),
        showlegend=False,
    )
    return fig


def scatter_map(df: pd.DataFrame) -> go.Figure:
    color_map = {"Baixo": "green", "Moderado": "yellow", "Alto": "orange", "Crítico": "red"}
    df = df.copy()
    df["color"] = df["risk_level"].map(color_map)
    fig = px.scatter_mapbox(
        df.sample(min(500, len(df))),
        lat="lat", lon="lon",
        color="risk_level",
        color_discrete_map=color_map,
        size="frp",
        size_max=15,
        zoom=3,
        center={"lat": -10, "lon": -55},
        mapbox_style="carto-darkmatter",
        hover_data={"state": True, "frp": True, "area_ha": True, "lat": False, "lon": False},
        title="Mapa de Focos (amostra)",
        template="plotly_dark",
        labels={"risk_level": "Risco"},
    )
    fig.update_layout(paper_bgcolor="#0e1117", margin=dict(t=40, b=0))
    return fig


def matplotlib_area_chart(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 3), facecolor="#0e1117")
    ax.set_facecolor("#0e1117")
    ax.fill_between(df["date"], df["area_total"], color="#e74c3c", alpha=0.4)
    ax.plot(df["date"], df["area_total"], color="#e74c3c", linewidth=1.5)
    ax.set_title("Área Total Queimada (ha) por Dia", color="white", fontsize=11)
    ax.tick_params(colors="gray")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.yaxis.label.set_color("gray")
    ax.xaxis.label.set_color("gray")
    plt.tight_layout()
    return fig
