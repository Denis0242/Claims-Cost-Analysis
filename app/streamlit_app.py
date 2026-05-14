# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Customer Risk Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    paths = [
        Path("data/customer_risk.csv"),
        Path("../data/customer_risk.csv"),
        Path("customer_risk.csv"),
        Path("data/customer_risk(1).csv"),
        Path("../data/customer_risk(1).csv")
    ]

    for path in paths:
        if path.exists():
            return pd.read_csv(path)

    st.error("CSV file not found. Put customer_risk.csv inside the data folder.")
    st.stop()


df = load_data()

# -----------------------------
# Clean / Prepare Data
# -----------------------------
df.columns = df.columns.str.strip().str.lower()

df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce").fillna(0)

# Create claim count per customer
claim_counts = (
    df.groupby("customer_id")["claim_id"]
    .count()
    .reset_index()
    .rename(columns={"claim_id": "claim_count"})
)

df = df.merge(claim_counts, on="customer_id", how="left")

# Create risk category using claim amount and claim frequency
high_loss_threshold = df["claim_amount"].quantile(0.75)
medium_loss_threshold = df["claim_amount"].quantile(0.50)
high_claim_threshold = df["claim_count"].quantile(0.75)

def assign_risk(row):
    if row["claim_amount"] >= high_loss_threshold or row["claim_count"] >= high_claim_threshold:
        return "High-risk"
    elif row["claim_amount"] >= medium_loss_threshold:
        return "Medium-risk"
    else:
        return "Low-risk"

df["risk_category"] = df.apply(assign_risk, axis=1)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#2F5F9F;'>Customer Risk Analysis Dashboard</h1>
    <p style='text-align:center; font-size:17px;'>
    Executive dashboard for monitoring customer risk exposure, claims behavior,
    loss concentration, and underwriting priorities.
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

region_filter = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique())
)

policy_filter = st.sidebar.multiselect(
    "Policy Type",
    sorted(df["policy_type"].dropna().unique()),
    default=sorted(df["policy_type"].dropna().unique())
)

age_filter = st.sidebar.multiselect(
    "Customer Age Band",
    sorted(df["customer_age_band"].dropna().unique()),
    default=sorted(df["customer_age_band"].dropna().unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    sorted(df["risk_category"].dropna().unique()),
    default=sorted(df["risk_category"].dropna().unique())
)

claim_threshold = st.sidebar.slider(
    "Claim Threshold",
    min_value=int(df["claim_count"].min()),
    max_value=int(df["claim_count"].max()),
    value=int(df["claim_count"].median())
)

loss_threshold = st.sidebar.slider(
    "Loss Threshold",
    min_value=int(df["claim_amount"].min()),
    max_value=int(df["claim_amount"].max()),
    value=int(df["claim_amount"].median())
)

filtered_df = df[
    (df["region"].isin(region_filter)) &
    (df["policy_type"].isin(policy_filter)) &
    (df["customer_age_band"].isin(age_filter)) &
    (df["risk_category"].isin(risk_filter))
]

# -----------------------------
# KPI Cards
# -----------------------------
total_customers = filtered_df["customer_id"].nunique()
avg_loss = filtered_df["claim_amount"].mean()
total_loss = filtered_df["claim_amount"].sum()

high_risk_df = filtered_df[filtered_df["risk_category"] == "High-risk"]

high_risk_pct = (
    high_risk_df["customer_id"].nunique() / total_customers * 100
    if total_customers > 0 else 0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Customers", f"{total_customers:,.0f}")
kpi2.metric("Avg Loss per Customer", f"${avg_loss:,.0f}")
kpi3.metric("Total Loss", f"${total_loss:,.0f}")
kpi4.metric("High Risk Customer %", f"{high_risk_pct:.2f}%")

st.divider()

# -----------------------------
# Dashboard Charts
# -----------------------------
left, center, right = st.columns([1.2, 1, 1])

with left:
    st.subheader("Claims vs Loss Segmentation")

    fig_scatter = px.scatter(
        filtered_df,
        x="claim_count",
        y="claim_amount",
        color="risk_category",
        hover_data=[
            "customer_id",
            "region",
            "policy_type",
            "customer_age_band",
            "claim_status"
        ],
        title="Claims Frequency vs Loss Amount"
    )

    fig_scatter.add_vline(
        x=claim_threshold,
        line_dash="dash",
        annotation_text="Claim Threshold"
    )

    fig_scatter.add_hline(
        y=loss_threshold,
        line_dash="dash",
        annotation_text="Loss Threshold"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

with center:
    st.subheader("Customer Risk Segmentation")

    risk_summary = (
        filtered_df.groupby("risk_category")["customer_id"]
        .nunique()
        .reset_index()
        .rename(columns={"customer_id": "customers"})
    )

    fig_donut = px.pie(
        risk_summary,
        names="risk_category",
        values="customers",
        hole=0.55,
        title="Customer Allocation by Risk Category"
    )

    st.plotly_chart(fig_donut, use_container_width=True)

with right:
    st.subheader("Claims Frequency by Age Band")

    age_summary = (
        filtered_df.groupby("customer_age_band")["claim_count"]
        .sum()
        .reset_index()
        .sort_values(by="claim_count", ascending=False)
    )

    fig_age = px.bar(
        age_summary,
        x="customer_age_band",
        y="claim_count",
        text="claim_count",
        title="Total Claims by Age Band"
    )

    fig_age.update_traces(textposition="outside")
    st.plotly_chart(fig_age, use_container_width=True)

# -----------------------------
# Second Row
# -----------------------------
row2_left, row2_mid, row2_right = st.columns([1, 1, 1.25])

with row2_left:
    st.subheader("Customer Allocation by Risk Category")

    fig_alloc = px.bar(
        risk_summary.sort_values("customers", ascending=False),
        x="risk_category",
        y="customers",
        color="risk_category",
        text="customers",
        title="Customers by Risk Segment"
    )

    fig_alloc.update_traces(textposition="outside")
    st.plotly_chart(fig_alloc, use_container_width=True)

with row2_mid:
    st.subheader("Loss Contribution by Risk Segment")

    loss_summary = (
        filtered_df.groupby("risk_category")["claim_amount"]
        .sum()
        .reset_index()
        .sort_values(by="claim_amount", ascending=True)
    )

    fig_loss = px.bar(
        loss_summary,
        x="claim_amount",
        y="risk_category",
        orientation="h",
        color="risk_category",
        text="claim_amount",
        title="Total Loss by Risk Segment"
    )

    fig_loss.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(fig_loss, use_container_width=True)

with row2_right:
    st.subheader("Customer Risk Detail Table")

    detail_df = filtered_df[
        [
            "customer_id",
            "region",
            "policy_type",
            "customer_age_band",
            "risk_category",
            "claim_count",
            "claim_amount",
            "claim_status"
        ]
    ].sort_values(by="claim_amount", ascending=False)

    st.dataframe(detail_df, use_container_width=True, height=410)

# -----------------------------
# Insight, Action, Recommendation, Decision
# -----------------------------
st.divider()
st.subheader("Executive Decision Summary")

high_risk_loss = high_risk_df["claim_amount"].sum()

high_risk_loss_pct = (
    high_risk_loss / total_loss * 100
    if total_loss > 0 else 0
)

top_region = (
    filtered_df.groupby("region")["claim_amount"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
    if len(filtered_df) > 0 else "N/A"
)

top_policy = (
    filtered_df.groupby("policy_type")["claim_amount"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
    if len(filtered_df) > 0 else "N/A"
)

box1, box2, box3, box4 = st.columns(4)

with box1:
    st.markdown("### 🔎 Insight")
    st.info(
        f"High-risk customers represent **{high_risk_pct:.2f}%** of the customer base "
        f"and contribute **{high_risk_loss_pct:.2f}%** of total loss exposure."
    )

with box2:
    st.markdown("### ⚙️ Action")
    st.warning(
        f"Monitor customers with claim frequency above **{claim_threshold}** "
        f"or claim losses above **${loss_threshold:,.0f}**."
    )

with box3:
    st.markdown("### ✅ Recommendation")
    st.success(
        f"Strengthen underwriting reviews for **{top_policy}** policies and prioritize "
        f"risk-control actions in the **{top_region}** region."
    )

with box4:
    st.markdown("### ⭐ Decision")
    st.error(
        "Prioritize high-risk customers for review, monitor medium-risk customers closely, "
        "and launch risk-mitigation programs to reduce future claim exposure."
    )

st.caption(
    "Dashboard focus: customer risk segmentation, claims behavior, loss concentration, underwriting action, and executive decision support."
)