import pandas as pd


def filter_fire_data(df: pd.DataFrame, states: list, biomes: list, risk_levels: list) -> pd.DataFrame:
    mask = (
        df["state"].isin(states) &
        df["biome"].isin(biomes) &
        df["risk_level"].isin(risk_levels)
    )
    return df[mask].copy()


def aggregate_by_day(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("date")
        .agg(total_focos=("frp", "count"), area_total=("area_ha", "sum"), frp_medio=("frp", "mean"))
        .reset_index()
    )


def aggregate_by_state(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("state")
        .agg(total_focos=("frp", "count"), area_total=("area_ha", "sum"))
        .reset_index()
        .sort_values("total_focos", ascending=False)
    )


def aggregate_by_risk(df: pd.DataFrame) -> pd.DataFrame:
    order = ["Baixo", "Moderado", "Alto", "Crítico"]
    result = df.groupby("risk_level").agg(count=("frp", "count")).reset_index()
    result["risk_level"] = pd.Categorical(result["risk_level"], categories=order, ordered=True)
    return result.sort_values("risk_level")


def merge_with_climate(fire_df: pd.DataFrame, climate_df: pd.DataFrame) -> pd.DataFrame:
    climate_agg = climate_df.groupby(["date", "state"]).agg(
        temperature=("temperature", "mean"),
        humidity=("humidity", "mean"),
    ).reset_index()
    return fire_df.merge(climate_agg, on=["date", "state"], how="left")
