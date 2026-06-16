import pandas as pd
import plotly.express as px
import streamlit as st


SEVERITY_ORDER = ["Low", "Medium", "High", "Critical"]


def kpi_card(label: str, value: str, help_text: str = "") -> None:
    with st.container(border=True):
        st.markdown(f"**{label}**")
        st.markdown(f"### {value}")
        if help_text:
            st.caption(help_text)


def claim_cost_by_region(df: pd.DataFrame):
    region_cost = (
        df.groupby("region", as_index=False)
        .agg(claim_amount=("claim_amount", "sum"))
        .sort_values("claim_amount", ascending=False)
    )
    return px.bar(region_cost, x="region", y="claim_amount", text_auto=".2s", title="Claim Cost by Region")


def claim_cost_by_type(df: pd.DataFrame):
    type_cost = (
        df.groupby("claim_type", as_index=False)
        .agg(claim_amount=("claim_amount", "sum"))
        .sort_values("claim_amount", ascending=False)
    )
    return px.bar(type_cost, x="claim_type", y="claim_amount", text_auto=".2s", title="Claim Cost by Claim Type")


def monthly_cost_trend(df: pd.DataFrame):
    monthly = (
        df.dropna(subset=["claim_date"])
        .set_index("claim_date")
        .resample("ME")["claim_amount"]
        .sum()
        .reset_index()
    )
    return px.line(monthly, x="claim_date", y="claim_amount", markers=True, title="Monthly Claim Cost Trend")
