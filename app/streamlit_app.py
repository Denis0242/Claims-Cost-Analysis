from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Insurance Claims Cost Analysis",
    page_icon="📊",
    layout="wide",
)


# -----------------------------
# Data loading and preparation
# -----------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and prepare the claims dataset from the project data folder."""
    data_path = Path(__file__).resolve().parents[1] / "data" / "claims_cost.csv"
    df = pd.read_csv(data_path)

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Date conversion
    if "claim_date" in df.columns:
        df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")

    # Numeric conversion
    if "claim_amount" in df.columns:
        df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce").fillna(0)

    # High-cost flag using 75th percentile
    if "high_cost_flag" not in df.columns and "claim_amount" in df.columns:
        threshold = df["claim_amount"].quantile(0.75)
        df["high_cost_flag"] = (df["claim_amount"] >= threshold).astype(int)

    # Cost band
    if "cost_band" not in df.columns and "claim_amount" in df.columns:
        df["cost_band"] = pd.cut(
            df["claim_amount"],
            bins=[-1, 1000, 3000, 6000, float("inf")],
            labels=["Low", "Medium", "High", "Very High"],
        )

    return df


# -----------------------------
# Helper functions
# -----------------------------
def safe_multiselect(label: str, df: pd.DataFrame, column: str):
    """Create a multiselect only when the selected column exists."""
    if column not in df.columns:
        return None

    values = sorted(df[column].dropna().unique())
    return st.multiselect(label, values, default=values)


def format_currency(value: float) -> str:
    """Format numeric values as currency."""
    return f"${value:,.0f}"


def format_compact_currency(value: float) -> str:
    """Format large currency values using K/M labels."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def format_compact_number(value: float) -> str:
    """Format values with K/M labels for chart data labels."""
    if pd.isna(value):
        return ""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def clean_chart_layout(fig, height: int | None = None):
    """Remove internal chart gridlines and apply a cleaner executive dashboard layout."""
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=25, t=70, b=45),
    )
    if height is not None:
        fig.update_layout(height=height)
    return fig


def calculate_yoy_delta(df: pd.DataFrame) -> float | None:
    """Calculate year-over-year percentage change in claim cost."""
    if not {"claim_date", "claim_amount"}.issubset(df.columns):
        return None

    temp = df.dropna(subset=["claim_date"]).copy()
    if temp.empty:
        return None

    temp["year"] = temp["claim_date"].dt.year
    yearly_cost = temp.groupby("year")["claim_amount"].sum().sort_index()

    if len(yearly_cost) < 2:
        return None

    prior_year_cost = yearly_cost.iloc[-2]
    current_year_cost = yearly_cost.iloc[-1]

    if prior_year_cost == 0:
        return None

    return ((current_year_cost - prior_year_cost) / prior_year_cost) * 100


def get_top_value(df: pd.DataFrame, group_col: str, amount_col: str = "claim_amount") -> tuple[str, float] | None:
    """Return the highest-cost category and amount."""
    if not {group_col, amount_col}.issubset(df.columns):
        return None

    summary = (
        df.groupby(group_col, as_index=False)[amount_col]
        .sum()
        .sort_values(amount_col, ascending=False)
    )

    if summary.empty:
        return None

    return str(summary.iloc[0][group_col]), float(summary.iloc[0][amount_col])


def add_section_header(title: str, description: str | None = None) -> None:
    """Add consistent section headings."""
    st.markdown("---")
    st.subheader(title)
    if description:
        st.caption(description)


# -----------------------------
# Main app
# -----------------------------
def main() -> None:
    df = load_data()

    st.title("Insurance Claims Cost Analysis")
    st.caption(
        "Executive dashboard for monitoring insurance claim cost drivers, "
        "regional exposure, severity patterns, and high-cost claims."
    )

    # Sidebar
    with st.sidebar:
        st.header("Filters")
        st.info(
            "Use this dashboard to monitor claim cost drivers, regional exposure, "
            "severity patterns, and underwriting risk."
        )

        selected_regions = safe_multiselect("Region", df, "region")
        selected_claim_types = safe_multiselect("Claim Type", df, "claim_type")
        selected_severities = safe_multiselect("Severity", df, "severity")

        date_range = None
        if "claim_date" in df.columns and df["claim_date"].notna().any():
            min_date = df["claim_date"].min().date()
            max_date = df["claim_date"].max().date()
            date_range = st.date_input("Claim Date Range", [min_date, max_date])

    # Apply filters
    filtered = df.copy()

    if selected_regions is not None:
        filtered = filtered[filtered["region"].isin(selected_regions)]

    if selected_claim_types is not None:
        filtered = filtered[filtered["claim_type"].isin(selected_claim_types)]

    if selected_severities is not None:
        filtered = filtered[filtered["severity"].isin(selected_severities)]

    if date_range is not None and len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered = filtered[
            (filtered["claim_date"] >= start_date)
            & (filtered["claim_date"] <= end_date)
        ]

    if filtered.empty:
        st.warning("No records match the selected filters.")
        return

    # KPI calculations
    total_cost = filtered["claim_amount"].sum() if "claim_amount" in filtered.columns else 0
    avg_cost = filtered["claim_amount"].mean() if "claim_amount" in filtered.columns else 0
    total_claims = filtered["claim_id"].nunique() if "claim_id" in filtered.columns else len(filtered)
    high_cost_share = (
        filtered["high_cost_flag"].mean() * 100
        if "high_cost_flag" in filtered.columns
        else 0
    )
    yoy_delta = calculate_yoy_delta(filtered)

    # KPI cards
    st.markdown("### Executive KPI Summary")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Claim Cost",
        format_compact_currency(total_cost),
        f"{yoy_delta:.1f}% YoY" if yoy_delta is not None else None,
    )
    col2.metric("Avg Claim Amount", format_currency(avg_cost))
    col3.metric("Total Claims", f"{total_claims:,.0f}")
    col4.metric("High-Cost Claim Share", f"{high_cost_share:.1f}%")

    # Auto insights
    top_region = get_top_value(filtered, "region")
    top_claim_type = get_top_value(filtered, "claim_type")
    top_severity = get_top_value(filtered, "severity")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    if top_region:
        insight_col1.info(
            f"**Top Region:** {top_region[0]}  \n"
            f"Cost Exposure: {format_currency(top_region[1])}"
        )

    if top_claim_type:
        insight_col2.info(
            f"**Top Claim Type:** {top_claim_type[0]}  \n"
            f"Cost Exposure: {format_currency(top_claim_type[1])}"
        )

    if top_severity:
        insight_col3.info(
            f"**Top Severity Level:** {top_severity[0]}  \n"
            f"Cost Exposure: {format_currency(top_severity[1])}"
        )

    # Download filtered data
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_claims_cost_analysis.csv",
        mime="text/csv",
    )

    # Claim cost segmentation
    add_section_header(
        "Claim Cost Segmentation",
        "Compare claim cost by region, claim type, and severity.",
    )

    # Full-width heatmap: gives this chart enough space and avoids the cramped two-column layout.
    if {"region", "claim_type", "claim_amount"}.issubset(filtered.columns):
        region_type = (
            filtered.groupby(["claim_type", "region"], as_index=False)
            .agg(claim_amount=("claim_amount", "sum"))
        )

        heatmap_values = (
            region_type.pivot(index="claim_type", columns="region", values="claim_amount")
            .fillna(0)
        )

        heatmap_labels = heatmap_values.copy()
        for col in heatmap_labels.columns:
            heatmap_labels[col] = heatmap_labels[col].apply(format_compact_number)

        fig = go.Figure(
            data=go.Heatmap(
                z=heatmap_values.values,
                x=heatmap_values.columns.tolist(),
                y=heatmap_values.index.tolist(),
                colorscale="Blues",
                colorbar={
                    "title": "Claim Cost",
                    "tickprefix": "$",
                    "tickformat": "~s",
                    "thickness": 14,
                    "len": 0.75,
                },
                hovertemplate=(
                    "Region: %{x}<br>"
                    "Claim Type: %{y}<br>"
                    "Claim Amount: $%{z:,.0f}<extra></extra>"
                ),
                xgap=5,
                ygap=5,
            )
        )

        # Add compact labels manually. This avoids Plotly text-property errors on older versions.
        for i, claim_type in enumerate(heatmap_values.index):
            for j, region in enumerate(heatmap_values.columns):
                fig.add_annotation(
                    x=region,
                    y=claim_type,
                    text=str(heatmap_labels.iloc[i, j]),
                    showarrow=False,
                    font=dict(size=13, color="black"),
                )

        fig.update_layout(
            title="Claim Cost by Region & Claim Type",
            xaxis_title="Region",
            yaxis_title="Claim Type",
            height=430,
            margin=dict(l=90, r=45, t=70, b=55),
        )
        fig.update_xaxes(side="bottom", showgrid=False, zeroline=False)
        fig.update_yaxes(showgrid=False, zeroline=False)
        clean_chart_layout(fig, height=430)
        st.plotly_chart(fig, use_container_width=True)

    # Severity comparison placed below the heatmap for a clearer view.
    if {"claim_type", "severity", "claim_amount"}.issubset(filtered.columns):
        type_cost = (
            filtered.groupby(["claim_type", "severity"], as_index=False)
            .agg(claim_amount=("claim_amount", "sum"))
        )

        type_cost["claim_amount_label"] = type_cost["claim_amount"].apply(format_compact_number)

        fig = px.bar(
            type_cost,
            x="claim_type",
            y="claim_amount",
            color="severity",
            title="Claim Type Comparison by Severity",
            text="claim_amount_label",
            labels={
                "claim_type": "Claim Type",
                "claim_amount": "Claim Amount",
                "severity": "Severity",
            },
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            yaxis_tickprefix="$",
            yaxis_tickformat="~s",
            height=470,
            bargap=0.28,
            legend_title_text="Severity",
            margin=dict(l=55, r=35, t=70, b=55),
        )
        clean_chart_layout(fig, height=470)
        st.plotly_chart(fig, use_container_width=True)

    # Trend over time
    add_section_header(
        "Cost Trend Over Time",
        "Monthly claim amount trend split by claim type.",
    )

    if {"claim_date", "claim_type", "claim_amount"}.issubset(filtered.columns):
        monthly_by_type = (
            filtered.dropna(subset=["claim_date"])
            .assign(claim_month=lambda data: data["claim_date"].dt.to_period("M").dt.to_timestamp())
            .groupby(["claim_month", "claim_type"], as_index=False)
            .agg(claim_amount=("claim_amount", "sum"))
        )

        monthly_by_type = monthly_by_type.sort_values(["claim_type", "claim_month"])
        monthly_by_type["point_order"] = monthly_by_type.groupby("claim_type").cumcount()
        monthly_by_type["last_point"] = (
            monthly_by_type.groupby("claim_type")["point_order"].transform("max")
        )
        monthly_by_type["claim_amount_label"] = monthly_by_type.apply(
            lambda row: format_compact_number(row["claim_amount"])
            if row["point_order"] == 0 or row["point_order"] == row["last_point"]
            else "",
            axis=1,
        )

        fig = px.line(
            monthly_by_type,
            x="claim_month",
            y="claim_amount",
            color="claim_type",
            markers=True,
            text="claim_amount_label",
            title="Monthly Claim Cost Trend by Claim Type",
            labels={
                "claim_month": "Date",
                "claim_amount": "Claim Amount",
                "claim_type": "Claim Type",
            },
        )
        fig.update_traces(
            texttemplate="%{text}",
            textposition="top center",
            hovertemplate=(
                "Date: %{x|%b %Y}<br>"
                "Claim Amount: $%{y:,.0f}<br>"
                "Claim Type: %{fullData.name}<extra></extra>"
            ),
        )
        fig.update_layout(
            yaxis_tickprefix="$",
            yaxis_tickformat="~s",
            legend_title_text="Claim Type",
        )
        clean_chart_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    elif {"claim_date", "claim_amount"}.issubset(filtered.columns):
        monthly = (
            filtered.dropna(subset=["claim_date"])
            .set_index("claim_date")
            .resample("ME")["claim_amount"]
            .sum()
            .reset_index()
        )

        monthly = monthly.sort_values("claim_date")
        monthly["claim_amount_label"] = ""
        if not monthly.empty:
            monthly.loc[monthly.index[0], "claim_amount_label"] = format_compact_number(monthly.loc[monthly.index[0], "claim_amount"])
            monthly.loc[monthly.index[-1], "claim_amount_label"] = format_compact_number(monthly.loc[monthly.index[-1], "claim_amount"])

        fig = px.line(
            monthly,
            x="claim_date",
            y="claim_amount",
            markers=True,
            text="claim_amount_label",
            title="Monthly Claim Cost Trend",
            labels={"claim_date": "Date", "claim_amount": "Claim Amount"},
        )
        fig.update_traces(texttemplate="%{text}", textposition="top center")
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat="~s")
        clean_chart_layout(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Severity and regional analysis
    add_section_header(
        "Severity & Regional Exposure",
        "Identify where claim cost concentration is highest.",
    )

    c1, c2 = st.columns([1, 1.45])

    with c1:
        if {"severity", "claim_amount"}.issubset(filtered.columns):
            severity_cost = (
                filtered.groupby("severity", as_index=False)
                .agg(
                    total_cost=("claim_amount", "sum"),
                    claim_count=("claim_amount", "count"),
                    avg_cost=("claim_amount", "mean"),
                )
                .sort_values("total_cost", ascending=False)
            )

            severity_cost["total_cost_label"] = severity_cost["total_cost"].apply(format_compact_number)

            fig = px.bar(
                severity_cost,
                x="severity",
                y="total_cost",
                text="total_cost_label",
                title="Claim Cost by Severity",
                labels={"severity": "Severity", "total_cost": "Total Claim Cost"},
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat="~s")
            clean_chart_layout(fig, height=460)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if {"region", "claim_amount"}.issubset(filtered.columns):
            region_cost = (
                filtered.groupby("region", as_index=False)
                .agg(claim_amount=("claim_amount", "sum"))
                .sort_values("claim_amount", ascending=False)
            )

            region_cost["claim_amount_label"] = region_cost["claim_amount"].apply(format_compact_number)

            fig = px.bar(
                region_cost,
                x="region",
                y="claim_amount",
                text="claim_amount_label",
                title="Claim Cost by Region",
                labels={"region": "Region", "claim_amount": "Claim Amount"},
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat="~s", bargap=0.35)
            clean_chart_layout(fig, height=520)
            st.plotly_chart(fig, use_container_width=True)

    # Broker risk exposure
    add_section_header(
        "Top Risk Broker Exposure",
        "Identify brokers with the highest claim cost concentration for underwriting review.",
    )

    if {"broker_id", "claim_amount"}.issubset(filtered.columns):
        broker_exposure = (
            filtered.groupby("broker_id", as_index=False)
            .agg(
                total_claim_cost=("claim_amount", "sum"),
                claim_count=("claim_amount", "count"),
                avg_claim_amount=("claim_amount", "mean"),
            )
            .sort_values("total_claim_cost", ascending=False)
            .head(10)
        )

        broker_exposure["total_claim_cost_label"] = broker_exposure["total_claim_cost"].apply(format_compact_number)

        fig = px.bar(
            broker_exposure,
            x="total_claim_cost",
            y="broker_id",
            orientation="h",
            text="total_claim_cost_label",
            title="Top 10 Broker Claim Cost Exposure",
            labels={
                "broker_id": "Broker ID",
                "total_claim_cost": "Total Claim Cost",
                "claim_count": "Claim Count",
                "avg_claim_amount": "Average Claim Amount",
            },
            hover_data={
                "total_claim_cost": ":,.0f",
                "claim_count": ":,.0f",
                "avg_claim_amount": ":,.0f",
            },
        )
        fig.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate=(
                "Broker ID: %{y}<br>"
                "Total Claim Cost: $%{x:,.0f}<br>"
                "<extra></extra>"
            ),
        )
        fig.update_layout(
            xaxis_tickprefix="$",
            xaxis_tickformat="~s",
            yaxis={"categoryorder": "total ascending"},
        )
        clean_chart_layout(fig, height=520)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View broker exposure detail"):
            broker_detail = broker_exposure.copy()
            broker_detail["total_claim_cost"] = broker_detail["total_claim_cost"].map("${:,.0f}".format)
            broker_detail["avg_claim_amount"] = broker_detail["avg_claim_amount"].map("${:,.0f}".format)
            st.dataframe(broker_detail, use_container_width=True)


    # High-cost claim review table reduced and placed inside an expander to keep the dashboard clean.
    add_section_header(
        "High-Cost Claim Review",
        "Top claims ranked by claim amount for underwriting and pricing review.",
    )

    with st.expander("View top 10 high-cost claims"):
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
            "cost_band",
        ]
        available_cols = [col for col in show_cols if col in filtered.columns]

        high_cost_table = (
            filtered.sort_values("claim_amount", ascending=False)[available_cols]
            .head(10)
            .copy()
        )

        if "claim_amount" in high_cost_table.columns:
            styled_table = high_cost_table.style.format({"claim_amount": "${:,.0f}"})
            st.dataframe(styled_table, use_container_width=True)
        else:
            st.dataframe(high_cost_table, use_container_width=True)

    # Executive summary
    st.markdown("---")
    st.markdown("## Executive Decision Summary")
    st.caption("Color-coded decision notes for business stakeholders.")

    decision_col1, decision_col2 = st.columns(2)

    with decision_col1:
        st.markdown(
            """
<div style="background-color:#E8F4FD; padding:18px; border-radius:12px; border-left:6px solid #1F77B4; margin-bottom:12px;">
<h4 style="margin-top:0;">🔎 Insight</h4>
<p style="margin-bottom:0;">Property claims, high-cost regions, and broker concentration drive the majority of claim cost exposure, creating pricing and underwriting risk.</p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div style="background-color:#FFF4E6; padding:18px; border-radius:12px; border-left:6px solid #FF7F0E; margin-bottom:12px;">
<h4 style="margin-top:0;">⚡ Action</h4>
<p style="margin-bottom:0;">Monitor property claims, regional cost concentration, high-severity claims, and brokers with repeated high-cost activity.</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with decision_col2:
        st.markdown(
            """
<div style="background-color:#EAF7EA; padding:18px; border-radius:12px; border-left:6px solid #2CA02C; margin-bottom:12px;">
<h4 style="margin-top:0;">✅ Recommendation</h4>
<p style="margin-bottom:0;">Adjust premiums in high-risk regions, improve underwriting rules for property policies, and investigate broker-level cost concentration.</p>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div style="background-color:#F3E8FF; padding:18px; border-radius:12px; border-left:6px solid #9467BD; margin-bottom:12px;">
<h4 style="margin-top:0;">🎯 Decision</h4>
<p style="margin-bottom:0;">Prioritize property policy pricing review, strengthen underwriting models, and review top broker exposure to control rising claim costs.</p>
</div>
""",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
