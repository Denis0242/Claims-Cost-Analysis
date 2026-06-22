# Insurance Claims Cost Analysis

## Executive Summary

This project analyzes insurance claim costs across regions, claim types, severity levels, and time periods to help insurance leadership identify high-cost drivers, improve underwriting decisions, and prioritize pricing actions.

The dashboard provides a centralized view of:

* **Total Claim Cost:** **$3,871,652**
* **Average Claim Amount:** **$3,872**
* **Total Claims:** **1,000**
* **YoY Cost Change:** **94.53% Increase**

The analysis highlights how **property claims**, **regional concentration**, and **severity patterns** influence insurance claim exposure and business risk.

---

# Business Problem

Insurance organizations face increasing claim costs driven by claim severity, regional concentration, and high-risk claim categories. Without centralized reporting, leadership may struggle to quickly identify:

* Which claim types create the largest financial exposure
* Which regions drive claim growth
* How severity impacts overall claim costs
* Where pricing and underwriting decisions should be adjusted
* Which loss drivers require immediate management attention

This project was designed to provide an executive-level decision-support dashboard that transforms raw claims data into actionable business insights for pricing, underwriting, risk management, and operational reporting.

---

# Decision Support Use Case

This dashboard supports insurance leadership, underwriting teams, risk managers, and claims operations teams by helping them:

* Monitor claim cost performance
* Identify high-risk claim categories
* Evaluate severity trends
* Detect regional loss concentration
* Prioritize underwriting interventions
* Support pricing strategy decisions
* Improve financial risk management

### Example Decisions Supported

* Should underwriting guidelines be adjusted for high-cost claim categories?
* Which regions require closer risk monitoring?
* Where should pricing reviews be prioritized?
* Which severity segments create the largest financial exposure?
* How should claims operations allocate risk management resources?

---

# KPIs

The dashboard tracks:

* Total Claim Cost
* Average Claim Amount
* Total Claims
* Year-over-Year (YoY) Cost Change
* Claim Cost by Region
* Claim Cost by Claim Type
* Severity Distribution
* Monthly Cost Trend
* High-Cost Claim Exposure

---

# Dashboard Overview

The dashboard provides a comprehensive view of insurance claim performance through:

* Executive KPI scorecards
* Regional claim cost analysis
* Claim type performance monitoring
* Severity distribution analysis
* Monthly cost trend reporting
* High-cost claim exposure tracking

The objective is to provide insurance leaders with a centralized reporting solution for monitoring financial risk and supporting data-driven decision-making.

---

# Dashboard Screenshots

## Dashboard Overview

![Dashboard Overview](screenshots/dashboard_overview.png)

## Executive KPI Summary

![KPI Summary](screenshots/kpi_summary.png)

## Claim Distribution by Region & Claim Type

![Claim Distribution](screenshots/claim_distribution.png)

## Claim Type Comparison

![Claim Type Comparison](screenshots/claim_type_comparison.png)

## Cost Trend Over Time

![Cost Trend](screenshots/cost_trend.png)

---

# Key Insights

Property claims and high-severity incidents account for the largest share of claim costs, representing the primary drivers of insurance loss exposure.

---

# Executive Decision Summary

## Insight

Property claims and high-severity incidents are the primary drivers of insurance loss exposure.

## Action

Increase monitoring of high-cost claim categories and regions with elevated loss activity.

## Recommendation

Review pricing models, underwriting criteria, and risk controls for the highest-cost segments.

## Decision

Prioritize risk management resources toward regions and claim categories generating the greatest financial impact.

---

# Business Impact

This project demonstrates how insurance organizations can use analytics to:

* Improve pricing decisions
* Strengthen underwriting strategies
* Monitor claim cost growth
* Reduce loss exposure
* Improve executive reporting
* Enhance financial risk visibility
* Support data-driven insurance operations

---

# Recommendations

Prioritize pricing reviews, underwriting controls, and risk monitoring efforts for high-cost claim categories and high-severity segments to reduce future loss exposure.

---

# Tools Used

**SQL • Tableau • Python • Pandas • Streamlit • Excel • Power Query**

---

# Repository Structure

```text
Claims-Cost-Risk-Analytics/
│── README.md
│── requirements.txt
│── streamlit_app.py
│
│── data/
│   ├── raw/
│   └── cleaned/
│
│── notebooks/
│   └── insurance_claims_eda.ipynb
│
│── screenshots/
│   ├── kpi_summary.png
│   ├── dashboard_overview.png
│   ├── claim_distribution.png
│   ├── claim_type_comparison.png
│   └── cost_trend.png
│
│── sql/
│   └── insurance_claim_queries.sql
```

---

# Data Dictionary

| Column       | Description                   |
| ------------ | ----------------------------- |
| claim_id     | Unique claim identifier       |
| claim_date   | Date claim was filed          |
| region       | Geographic claim region       |
| claim_type   | Insurance claim category      |
| severity     | Claim severity classification |
| claim_amount | Monetary value of the claim   |
| policy_id    | Policy identifier             |
| customer_id  | Customer identifier           |
| broker_id    | Broker identifier             |
| claim_status | Current claim status          |

---

# Dataset Overview

| Metric       | Details                                                 |
| ------------ | ------------------------------------------------------- |
| Dataset Size | 1,000 Rows                                              |
| Columns      | 16                                                      |
| Date Range   | 2024-01-01 → 2025-12-31                                 |
| Industry     | Insurance                                               |
| Dataset Type | Synthetic Insurance Claims Dataset                      |
| Use Case     | Cost Monitoring, Risk Segmentation, Executive Reporting |

### Key Fields

* Claim ID
* Claim Date
* Region
* Claim Type
* Severity
* Claim Amount
* Policy ID
* Customer ID
* Broker ID
* Claim Status

---

# EDA & Data Cleaning

The exploratory data analysis (EDA) and cleaning process is documented in:

```text
notebooks/insurance_claims_eda.ipynb
```

### Data Cleaning Workflow

#### Data Validation

* Checked dataset structure and column consistency
* Reviewed data types for numeric and categorical fields
* Converted claim dates into datetime format

#### Data Quality Checks

* Checked missing values
* Removed duplicate records
* Validated claim amount ranges
* Standardized categorical values

#### Feature Engineering

Created additional analytical fields:

* Month
* Quarter
* Year
* High-Cost Claim Flag
* Cost Band Categories
* Claim Severity Segments

#### EDA Analysis

* Claim distribution by region
* Claim cost by claim type
* Severity analysis
* Monthly cost trends
* Outlier detection
* Cost concentration analysis

---

# How to Run the Project

## Clone Repository

```bash
git clone https://github.com/yourusername/Claims-Cost-Risk-Analytics.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Streamlit Application

```bash
streamlit run streamlit_app.py
```

---

# Disclaimer

This project uses a synthetic insurance claims dataset created for portfolio and educational purposes.

No real customer, policyholder, broker, or insurance company information is included.

The dashboard is intended solely to demonstrate analytics, reporting, business intelligence, and decision-support capabilities.
