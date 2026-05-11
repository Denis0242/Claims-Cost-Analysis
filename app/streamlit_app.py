from pathlib import Path
import pandas as pd
import streamlit as st

from components import insight_panel, metric_card
from utils import calculate_kpis, load_claims_data

st.set_page_config(page_title="Insurance Claims Cost Analysis", layout="wide")
st.title("Insurance Claims Cost Analysis")
st.caption("Executive claims intelligence dashboard for cost, region, severity, and claim-type analysis")

ROOT = Path(__file__).resolve().parents[1]
df = load_claims_data(str(ROOT / "data" / "claims_cost.csv"))

with st.sidebar:
    st.header("Filters")
    region = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    claim_type = st.multiselect("Claim Type", sorted(df["claim_type"].unique()), default=sorted(df["claim_type"].unique()))
    severity = st.multiselect("Severity", sorted(df["severity"].unique()), default=sorted(df["severity"].unique()))

filtered = df[df["region"].isin(region) & df["claim_type"].isin(claim_type) & df["severity"].isin(severity)]
kpis = calculate_kpis(filtered)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Total Claim Cost", f"${kpis['total_cost']:,.0f}")
with c2:
    metric_card("Avg Claim Amount", f"${kpis['avg_claim']:,.0f}")
with c3:
    metric_card("Total Claims", f"{kpis['total_claims']:,.0f}")
with c4:
    yoy_value = "N/A" if kpis["yoy"] is None else f"{kpis['yoy']:.2%}"
    metric_card("YoY % Change", yoy_value)

st.divider()

left, right = st.columns([1, 1])
with left:
    st.subheader("Claim Cost by Region")
    region_cost = filtered.groupby("region", as_index=False)["claim_amount"].sum().sort_values("claim_amount", ascending=False)
    st.bar_chart(region_cost.set_index("region"))

with right:
    st.subheader("Claim Cost by Claim Type")
    type_cost = filtered.groupby("claim_type", as_index=False)["claim_amount"].sum().sort_values("claim_amount", ascending=False)
    st.bar_chart(type_cost.set_index("claim_type"))

st.subheader("Monthly Cost Trend")
monthly = filtered.groupby("claim_month_start", as_index=False)["claim_amount"].sum()
st.line_chart(monthly.set_index("claim_month_start"))

st.subheader("Region x Claim Type Cost Matrix")
matrix = pd.pivot_table(filtered, values="claim_amount", index="claim_type", columns="region", aggfunc="sum", fill_value=0)
st.dataframe(matrix.style.format("${:,.0f}"), use_container_width=True)

insight_panel()

st.subheader("Data Preview")
st.dataframe(filtered.head(100), use_container_width=True)
