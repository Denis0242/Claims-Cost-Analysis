from pathlib import Path
import numpy as np
import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_raw_data() -> pd.DataFrame:
    data_path = project_root() / "data" / "customer_risk.csv"
    return pd.read_csv(data_path)


def clean_customer_risk_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean customer-risk data and return cleaned rows + cleaning audit."""
    audit_rows = []
    df = raw.copy()
    audit_rows.append({"step": "Raw rows loaded", "records": len(df), "issue_fixed": "Baseline source file imported"})

    original_columns = list(df.columns)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    audit_rows.append({"step": "Standardized column names", "records": len(df), "issue_fixed": f"{len(original_columns)} columns normalized to snake_case"})

    duplicate_claims = int(df.duplicated(subset=["claim_id"]).sum()) if "claim_id" in df.columns else 0
    df = df.drop_duplicates(subset=["claim_id"]).copy()
    audit_rows.append({"step": "Removed duplicate claim IDs", "records": len(df), "issue_fixed": f"{duplicate_claims} duplicate claim rows removed"})

    missing_before = int(df.isna().sum().sum())
    required_text = ["claim_id", "customer_id", "region", "policy_type", "customer_age_band", "claim_status"]
    for col in required_text:
        df[col] = df[col].astype(str).str.strip().replace({"": np.nan, "nan": np.nan, "None": np.nan})
    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
    for col in ["tenure_years", "annual_premium", "claim_amount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["claim_id", "customer_id", "claim_date", "region", "policy_type", "customer_age_band", "claim_amount"])
    audit_rows.append({"step": "Handled missing and invalid values", "records": len(df), "issue_fixed": f"{missing_before} missing cells reviewed; critical incomplete rows removed"})

    invalid_amounts = int(((df["claim_amount"] < 0) | (df["annual_premium"] < 0)).sum())
    df = df[(df["claim_amount"] >= 0) & (df["annual_premium"] >= 0)].copy()
    audit_rows.append({"step": "Validated numeric ranges", "records": len(df), "issue_fixed": f"{invalid_amounts} negative claim/premium rows removed"})

    df["region"] = df["region"].str.title()
    df["policy_type"] = df["policy_type"].str.title()
    df["claim_status"] = df["claim_status"].str.title()
    df["loss_ratio"] = np.where(df["annual_premium"] > 0, df["claim_amount"] / df["annual_premium"], np.nan)
    df["claim_month"] = df["claim_date"].dt.to_period("M").astype(str)
    audit_rows.append({"step": "Created analysis-ready fields", "records": len(df), "issue_fixed": "Added loss_ratio and claim_month for EDA/dashboard analysis"})

    return df, pd.DataFrame(audit_rows)


def build_customer_summary(cleaned: pd.DataFrame, claim_threshold: int = 4, loss_threshold: float = 15000) -> pd.DataFrame:
    def first_mode(series):
        mode = series.mode(dropna=True)
        return mode.iloc[0] if not mode.empty else series.iloc[0]

    customer = cleaned.groupby("customer_id", as_index=False).agg(
        region=("region", first_mode),
        policy_type=("policy_type", first_mode),
        customer_age_band=("customer_age_band", first_mode),
        claims_count=("claim_id", "nunique"),
        total_loss=("claim_amount", "sum"),
        avg_loss=("claim_amount", "mean"),
        annual_premium=("annual_premium", "mean"),
        first_claim_date=("claim_date", "min"),
        last_claim_date=("claim_date", "max"),
    )
    customer["loss_ratio"] = np.where(customer["annual_premium"] > 0, customer["total_loss"] / customer["annual_premium"], np.nan)

    customer["risk_category"] = np.select(
        [
            (customer["claims_count"] >= claim_threshold) | (customer["total_loss"] >= loss_threshold),
            (customer["claims_count"] >= max(2, claim_threshold // 2)) | (customer["total_loss"] >= loss_threshold * 0.50),
        ],
        ["High-risk", "Medium-risk"],
        default="Low-risk",
    )
    return customer


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_pct(value: float) -> str:
    return f"{value:.2f}%"
