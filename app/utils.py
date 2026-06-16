from pathlib import Path

import numpy as np
import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_claims_data(filename: str = "claims_cost.csv") -> pd.DataFrame:
    data_path = project_root() / "data" / filename
    df = pd.read_csv(data_path)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def clean_claims_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean claims data and return cleaned rows plus a cleaning audit table."""
    audit_rows = []
    df = raw.copy()

    audit_rows.append(
        {"step": "Raw rows loaded", "records": len(df), "issue_fixed": "Baseline source file imported"}
    )

    original_columns = list(df.columns)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    audit_rows.append(
        {
            "step": "Standardized column names",
            "records": len(df),
            "issue_fixed": f"{len(original_columns)} columns normalized to snake_case",
        }
    )

    if "claim_id" in df.columns:
        duplicate_claims = int(df.duplicated(subset=["claim_id"]).sum())
        df = df.drop_duplicates(subset=["claim_id"]).copy()
    else:
        duplicate_claims = 0

    audit_rows.append(
        {
            "step": "Removed duplicate claim IDs",
            "records": len(df),
            "issue_fixed": f"{duplicate_claims} duplicate claim rows removed",
        }
    )

    missing_before = int(df.isna().sum().sum())

    for col in ["claim_id", "customer_id", "region", "claim_type", "severity", "claim_status"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"": np.nan, "nan": np.nan, "None": np.nan})

    if "claim_date" in df.columns:
        df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")

    if "claim_amount" in df.columns:
        df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce")

    required_cols = [col for col in ["claim_id", "claim_date", "region", "claim_type", "severity", "claim_amount"] if col in df.columns]
    if required_cols:
        df = df.dropna(subset=required_cols)

    audit_rows.append(
        {
            "step": "Handled missing and invalid values",
            "records": len(df),
            "issue_fixed": f"{missing_before} missing cells reviewed; critical incomplete rows removed",
        }
    )

    if "claim_amount" in df.columns:
        invalid_amounts = int((df["claim_amount"] < 0).sum())
        df = df[df["claim_amount"] >= 0].copy()
    else:
        invalid_amounts = 0

    audit_rows.append(
        {
            "step": "Validated numeric ranges",
            "records": len(df),
            "issue_fixed": f"{invalid_amounts} negative claim amount rows removed",
        }
    )

    for col in ["region", "claim_type", "severity", "claim_status"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    if "claim_date" in df.columns:
        df["claim_month"] = df["claim_date"].dt.to_period("M").astype(str)
        df["claim_year"] = df["claim_date"].dt.year

    if "claim_amount" in df.columns:
        threshold = df["claim_amount"].quantile(0.75)
        df["high_cost_flag"] = (df["claim_amount"] >= threshold).astype(int)
        df["cost_band"] = pd.cut(
            df["claim_amount"],
            bins=[-1, 1000, 3000, 6000, float("inf")],
            labels=["Low", "Medium", "High", "Very High"],
        )

    audit_rows.append(
        {
            "step": "Created analysis-ready fields",
            "records": len(df),
            "issue_fixed": "Added claim_month, claim_year, high_cost_flag, and cost_band for dashboard analysis",
        }
    )

    return df, pd.DataFrame(audit_rows)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_pct(value: float) -> str:
    return f"{value:.2f}%"
