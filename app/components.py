import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

RISK_ORDER = ["High-risk", "Medium-risk", "Low-risk"]
RISK_COLOR_MAP = {"High-risk": "#E45756", "Medium-risk": "#F28E2B", "Low-risk": "#4E79A7"}


def kpi_card(label: str, value: str, status: str = "", help_text: str = ""):
    with st.container(border=True):
        st.markdown(f"<div style='font-size:0.95rem;color:#3B6EA8;text-align:center'>{label}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.55rem;font-weight:700;text-align:center'>{value}</div>", unsafe_allow_html=True)
        if status:
            badge_color = "#E45756" if status.lower() == "bad" else "#59A14F"
            st.markdown(f"<div style='text-align:center;color:{badge_color};font-weight:700'>■ {status}</div>", unsafe_allow_html=True)
        if help_text:
            st.caption(help_text)


def donut_chart(customer_summary: pd.DataFrame):
    counts = customer_summary["risk_category"].value_counts().reindex(RISK_ORDER, fill_value=0).reset_index()
    counts.columns = ["risk_category", "customers"]
    fig = px.pie(
        counts, names="risk_category", values="customers", hole=0.55,
        color="risk_category", color_discrete_map=RISK_COLOR_MAP,
        title="Customer Risk Segmentation"
    )
    fig.update_traces(textposition="outside", textinfo="label+percent")
    fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=55, b=10))
    return fig


def claims_vs_loss_scatter(customer_summary: pd.DataFrame, claim_threshold: int, loss_threshold: float):
    fig = px.scatter(
        customer_summary, x="claims_count", y="total_loss", color="risk_category",
        size="avg_loss", hover_data=["customer_id", "region", "policy_type", "customer_age_band"],
        color_discrete_map=RISK_COLOR_MAP, title="Claims vs Loss Segmentation"
    )
    fig.add_vline(x=claim_threshold, line_dash="dash", annotation_text="Claim Threshold")
    fig.add_hline(y=loss_threshold, line_dash="dash", annotation_text="Loss Threshold")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=55, b=10))
    return fig


def claims_frequency_by_age(cleaned_claims: pd.DataFrame):
    age_order = ["18-29", "30-44", "45-59", "60+"]
    age = cleaned_claims.groupby("customer_age_band", as_index=False).agg(claims=("claim_id", "nunique"))
    age["customer_age_band"] = pd.Categorical(age["customer_age_band"], categories=age_order, ordered=True)
    age = age.sort_values("customer_age_band")
    fig = px.bar(age, x="customer_age_band", y="claims", text="claims", title="Claims Frequency by Age Band")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=330, xaxis_title="", yaxis_title="Claims", margin=dict(l=10, r=10, t=55, b=10))
    return fig


def customer_allocation(customer_summary: pd.DataFrame):
    allocation = customer_summary["risk_category"].value_counts().reindex(RISK_ORDER, fill_value=0).reset_index()
    allocation.columns = ["risk_category", "customers"]
    fig = px.bar(allocation, x="risk_category", y="customers", color="risk_category", text="customers", color_discrete_map=RISK_COLOR_MAP, title="Customer Allocation by Risk Category")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=330, showlegend=False, xaxis_title="", yaxis_title="Customers", margin=dict(l=10, r=10, t=55, b=10))
    return fig


def loss_contribution(customer_summary: pd.DataFrame):
    loss = customer_summary.groupby("risk_category", as_index=False).agg(total_loss=("total_loss", "sum"))
    loss["risk_category"] = pd.Categorical(loss["risk_category"], categories=RISK_ORDER, ordered=True)
    loss = loss.sort_values("risk_category")
    fig = px.bar(loss, y="risk_category", x="total_loss", orientation="h", color="risk_category", text="total_loss", color_discrete_map=RISK_COLOR_MAP, title="Loss Contribution by Risk Segment")
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(height=330, showlegend=False, xaxis_title="Total Loss", yaxis_title="", margin=dict(l=10, r=10, t=55, b=10))
    return fig
