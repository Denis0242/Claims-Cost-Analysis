import pandas as pd


def load_claims_data(path: str = "data/claims_cost.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["claim_date"])
    df["claim_month_start"] = df["claim_date"].dt.to_period("M").dt.to_timestamp()
    return df


def calculate_kpis(df: pd.DataFrame) -> dict:
    total_cost = df["claim_amount"].sum()
    total_claims = df["claim_id"].nunique()
    avg_claim = df["claim_amount"].mean()
    yearly = df.groupby("claim_year")["claim_amount"].sum().sort_index()
    yoy = None
    if len(yearly) >= 2 and yearly.iloc[-2] != 0:
        yoy = (yearly.iloc[-1] - yearly.iloc[-2]) / yearly.iloc[-2]
    return {
        "total_cost": total_cost,
        "total_claims": total_claims,
        "avg_claim": avg_claim,
        "yoy": yoy,
    }
