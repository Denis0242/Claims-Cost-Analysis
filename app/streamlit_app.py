import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Insurance Claims Cost Analysis", layout="wide")

@st.cache_data
def load_data():
    app_path = Path(__file__).resolve()
    data_path = app_path.parents[1] / "data" / "claims_cost.csv"
    df = pd.read_csv(data_path)

    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
    df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce").fillna(0)

    if "high_cost_flag" not in df.columns:
        df["high_cost_flag"] = (df["claim_amount"] >= df["claim_amount"].quantile(0.75)).astype(int)

    return df

df = load_data()

st.title("Insurance Claims Cost Analysis")
st.caption("Tableau-style Streamlit recreation for executive claim cost monitoring")

with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        sorted(df["region"].dropna().unique()),
        default=sorted(df["region"].dropna().unique())
    )

    claim_types = st.multiselect(
        "Claim Type",
        sorted(df["claim_type"].dropna().unique()),
        default=sorted(df["claim_type"].dropna().unique())
    )

    severities = st.multiselect(
        "Severity",
        sorted(df["severity"].dropna().unique()),
        default=sorted(df["severity"].dropna().unique())
    )

    min_date = df["claim_date"].min()
    max_date = df["claim_date"].max()

    date_range = st.date_input(
        "Claim Date Range",
        [min_date.date(), max_date.date()]
    )

filtered = df[
    df["region"].isin(regions)
    & df["claim_type"].isin(claim_types)
    & df["severity"].isin(severities)
].copy()

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    filtered = filtered[
        (filtered["claim_date"] >= start_date)
        & (filtered["claim_date"] <= end_date)
    ]

col1, col2, col3, col4 = st.columns(4)

total_cost = filtered["claim_amount"].sum()
avg_cost = filtered["claim_amount"].mean() if len(filtered) else 0
total_claims = filtered["claim_id"].nunique() if "claim_id" in filtered.columns else len(filtered)
high_cost_share = filtered["high_cost_flag"].mean() * 100 if len(filtered) else 0

col1.metric("Total Claim Cost", f"${total_cost:,.0f}")
col2.metric("Avg Claim Amount", f"${avg_cost:,.0f}")
col3.metric("Total Claims", f"{total_claims:,.0f}")
col4.metric("High-Cost Claim Share", f"{high_cost_share:.1f}%")

st.divider()

left, right = st.columns([1.1, 1])

with left:
    region_type = (
        filtered
        .groupby(["region", "claim_type"], as_index=False)
        .agg(claim_amount=("claim_amount", "sum"))
    )

    fig = px.density_heatmap(
        region_type,
        x="region",
        y="claim_type",
        z="claim_amount",
        text_auto=True,
        title="Claim Distribution by Region & Claim Type"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    type_cost = (
        filtered
        .groupby(["claim_type", "severity"], as_index=False)
        .agg(claim_amount=("claim_amount", "sum"))
    )

    fig = px.bar(
        type_cost,
        x="claim_type",
        y="claim_amount",
        color="severity",
        title="Claim Type Comparison",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

monthly = (
    filtered
    .dropna(subset=["claim_date"])
    .set_index("claim_date")
    .resample("ME")["claim_amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="claim_date",
    y="claim_amount",
    markers=True,
    title="Cost Trend Over Time"
)
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    severity_cost = (
        filtered
        .groupby("severity", as_index=False)
        .agg(
            total_cost=("claim_amount", "sum"),
            claim_count=("claim_amount", "count"),
            avg_cost=("claim_amount", "mean")
        )
    )

    fig = px.bar(
        severity_cost,
        x="severity",
        y="total_cost",
        text_auto=".2s",
        title="Claim Cost by Severity"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    region_cost = (
        filtered
        .groupby("region", as_index=False)
        .agg(claim_amount=("claim_amount", "sum"))
        .sort_values("claim_amount", ascending=False)
    )

    fig = px.bar(
        region_cost,
        x="region",
        y="claim_amount",
        text_auto=".2s",
        title="Claim Cost by Region"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("High-Cost Claim Review")

show_cols = [
    "claim_id",
    "claim_date",
    "region",
    "claim_type",
    "severity",
    "claim_status",
    "policy_id",
    "customer_id",
    "broker_id",
    "claim_amount",
    "cost_band"
]

available_cols = [col for col in show_cols if col in filtered.columns]

st.dataframe(
    filtered.sort_values("claim_amount", ascending=False)[available_cols],
    use_container_width=True
)

st.divider()

st.markdown("## Executive Decision Summary")

st.markdown("""
<style>
.summary-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-top: 20px;
}
.summary-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 14px;
}
.summary-card {
    padding: 22px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
    min-height: 190px;
}
.insight-card {
    background-color: #E8F2FF;
    color: #0057B8;
}
.action-card {
    background-color: #FFFDE7;
    color: #8A6500;
}
.recommendation-card {
    background-color: #E6F7EC;
    color: #087B32;
}
.decision-card {
    background-color: #FDE7E9;
    color: #B3262E;
}
</style>

<div class="summary-container">

<div>
    <div class="summary-title">🔎 Insight</div>
    <div class="summary-card insight-card">
        Property claims and high-growth regions drive the majority of claim cost exposure, creating pricing and underwriting risk.
    </div>
</div>

<div>
    <div class="summary-title">⚙️ Action</div>
    <div class="summary-card action-card">
        Monitor property claims, regional cost concentration, high-severity claims, and brokers with repeated high-cost activity.
    </div>
</div>

<div>
    <div class="summary-title">✅ Recommendation</div>
    <div class="summary-card recommendation-card">
        Adjust premiums in high-risk regions, improve underwriting rules for property policies, and investigate high-cost claim patterns.
    </div>
</div>

<div>
    <div class="summary-title">⭐ Decision</div>
    <div class="summary-card decision-card">
        Prioritize property policy pricing review and strengthen underwriting models to control rising claim costs.
    </div>
</div>

</div>
""", unsafe_allow_html=True)