# Insurance Claims Cost Analysis

## Executive Summary

This project analyzes insurance claim costs across regions, claim types, severity levels, and time periods to help insurance leadership identify high-cost drivers, improve underwriting decisions, and prioritize pricing actions.

The dashboard provides a centralized view of insurance claim performance through financial, operational, and risk-focused KPIs.

Key results include:

* Total Claim Cost: $3,871,652
* Average Claim Amount: $3,872
* Total Claims: 1,000
* Year-over-Year Cost Change: 94.53% Increase

The analysis highlights how claim severity, regional concentration, and claim type distribution influence insurance loss exposure and financial risk.

Built using SQL, Tableau, Python, Streamlit, Excel, and Power Query.

---

# Business Problem

Insurance organizations face increasing claim costs driven by:

* High-severity claims
* Regional loss concentration
* Rising claim frequency
* High-cost claim categories
* Inefficient pricing and underwriting decisions

Without centralized reporting, leadership teams may struggle to identify:

* High-risk claim categories
* Cost concentration trends
* Regional loss exposure
* Underwriting improvement opportunities
* Pricing strategy adjustments

This project provides an executive-level decision-support solution that transforms insurance claims data into actionable business insights.

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

The dashboard answers key business questions such as:

* Which claim types create the largest financial exposure?
* Which regions require closer monitoring?
* Which severity levels contribute most to losses?
* Where should pricing reviews be prioritized?
* How should risk management resources be allocated?

---

# KPIs

The dashboard monitors:

| KPI                      | Business Purpose                    |
| ------------------------ | ----------------------------------- |
| Total Claim Cost         | Measures overall financial exposure |
| Average Claim Amount     | Measures average claim severity     |
| Total Claims             | Measures claim volume               |
| YoY Cost Change          | Measures cost growth trends         |
| Claim Cost by Region     | Identifies regional exposure        |
| Claim Cost by Claim Type | Identifies category exposure        |
| Severity Distribution    | Measures risk concentration         |
| Monthly Cost Trend       | Tracks claim cost performance       |
| High-Cost Claim Exposure | Identifies major financial risk     |

---

# Dashboard Overview

The dashboard provides a comprehensive view of insurance claim performance through:

* Executive KPI Monitoring
* Regional Claim Cost Analysis
* Claim Type Performance Evaluation
* Severity Distribution Monitoring
* Monthly Cost Trend Reporting
* High-Cost Claim Exposure Tracking

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

# Key Insight

Property claims and high-severity incidents account for the largest share of claim costs, making them the primary drivers of insurance loss exposure and financial risk.

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

The dashboard provides leadership teams with actionable visibility into claim performance and loss concentration.

---

# Recommendation

Prioritize pricing reviews, underwriting controls, and risk monitoring efforts for high-cost claim categories and high-severity segments to reduce future loss exposure and improve financial performance.

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

# SQL Queries

The repository includes SQL queries supporting:

* KPI Analysis
* Regional Claim Cost Analysis
* Severity Evaluation
* Claim Type Performance Analysis
* High-Cost Claim Identification

SQL File:

```text id="4ld8vv"
sql/insurance_claim_queries.sql
```

---

# EDA + Feature Engineering

The exploratory data analysis and feature engineering process includes:

### Data Validation

* Dataset structure review
* Data type validation
* Date formatting validation

### Data Quality Checks

* Missing value assessment
* Duplicate record validation
* Claim amount range validation
* Categorical value standardization

### Feature Engineering

Created analytical fields including:

* Month
* Quarter
* Year
* High-Cost Claim Flag
* Cost Band Categories
* Claim Severity Segments

### Exploratory Analysis

* Claim distribution by region
* Claim cost by claim type
* Severity analysis
* Monthly trend analysis
* Outlier identification
* Cost concentration analysis

---

# Analytics Workflow

```text id="k30s3l"
Business Problem
        ↓
EDA + Cleaning
        ↓
Feature Engineering
        ↓
SQL Transformations
        ↓
Risk Analysis
        ↓
Dashboard Development
        ↓
Business Insights
        ↓
Decision Support
        ↓
Business Impact
```

---

# Executive Decision Summary

### Insight

Property claims and high-severity incidents are the primary drivers of insurance loss exposure and claim cost growth.

### Action

Increase monitoring of high-cost claim categories and regions with elevated loss activity.

### Recommendation

Review pricing models, underwriting criteria, and risk controls for the highest-cost claim segments.

### Decision

Prioritize risk management resources toward regions and claim categories generating the greatest financial impact.

---

# Tools Used

* SQL
* Tableau
* Python
* Pandas
* Streamlit
* Excel
* Power Query
* GitHub

---

# Repository Structure

```text id="t6w4kh"
Claims-Cost-Risk-Analytics/

├── README.md
├── requirements.txt
├── streamlit_app.py

├── data/
│   ├── raw/
│   └── cleaned/

├── notebooks/
│   └── insurance_claims_eda.ipynb

├── screenshots/
│   ├── dashboard_overview.png
│   ├── kpi_summary.png
│   ├── claim_distribution.png
│   ├── claim_type_comparison.png
│   └── cost_trend.png

├── sql/
│   └── insurance_claim_queries.sql
```

---

# How to Run the Project

## Clone Repository

```bash id="mjtdv6"
git clone https://github.com/yourusername/Claims-Cost-Risk-Analytics.git
```

## Install Dependencies

```bash id="yhfrru"
pip install -r requirements.txt
```

## Launch Streamlit App

```bash id="07a1m9"
streamlit run streamlit_app.py
```

---

# Disclaimer

* Dataset is synthetic and created for portfolio purposes.
* No real customer, broker, policyholder, or insurance company information is included.
* Project developed for educational and demonstration purposes.
* Business impact examples are illustrative and intended to demonstrate analytical decision-making.
