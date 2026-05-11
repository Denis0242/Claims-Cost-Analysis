# Insurance Claims Cost Analysis

## Executive Summary

This repository is a full analytics decision-support project built from an insurance claims dataset and Tableau dashboard screenshot. The project analyzes claim cost, claim volume, regional risk, claim-type concentration, year-over-year cost movement, and underwriting opportunities.

**Dashboard headline:** total claim cost is **$3,871,652** across **1,000 claims**, with an average claim amount of **$3,872**. The highest-cost claim type is **Property**, and the highest-cost region is **South**. Year-over-year claim cost changed by approximately **94.53%**.

![Insurance Claims Cost Dashboard](screenshots/insurance_claims_cost_dashboard.png)

---

## Business Problem

Insurance leaders need to understand where claim costs are increasing, which claim types are driving financial exposure, and which regions require pricing, underwriting, or claims-management intervention. Without a clear cost intelligence workflow, teams may react late to rising loss pressure and miss opportunities to improve pricing discipline.

---

## KPI Goals

| KPI | Purpose |
|---|---|
| Total Claim Cost | Measures total financial exposure |
| Average Claim Amount | Tracks claim severity and cost per incident |
| Total Claims | Measures claim volume |
| YoY % Change | Identifies cost acceleration or improvement |
| Claim Type Cost | Shows which products/policies drive losses |
| Regional Cost Distribution | Identifies high-risk geographic segments |
| Severity Mix | Supports underwriting and claims triage |

---

## Dataset

The dataset contains **1,000 claim records** with claim dates, year/month fields, region, claim type, severity, claim status, policy ID, customer ID, broker ID, and claim amount.

**Main fields:**

```text
claim_id, claim_date, claim_year, claim_month, region, claim_type,
severity, claim_status, policy_id, customer_id, broker_id, claim_amount
```

---

## SQL Transformations

SQL files are included in the `sql/` folder for:

- KPI summary reporting
- Regional cost and claim distribution
- Claim type cost comparison
- Severity risk analysis
- Monthly trend analysis
- YoY cost movement

---

## Metrics Engineering

Core calculations used in this project:

```text
Total Claim Cost = SUM(claim_amount)
Average Claim Amount = AVG(claim_amount)
Total Claims = COUNT(DISTINCT claim_id)
YoY % Change = (Current Year Claim Cost - Prior Year Claim Cost) / Prior Year Claim Cost
Region Share = Region Claim Cost / Total Claim Cost
Claim Type Share = Claim Type Claim Cost / Total Claim Cost
```

---

## Analytics Workflow

1. Load raw claims data from CSV.
2. Clean and validate date, region, claim type, severity, and claim amount fields.
3. Aggregate claims by region, type, severity, and month.
4. Build KPI logic for claim amount, average amount, total claims, and YoY change.
5. Create Tableau dashboard for executive analysis.
6. Convert findings into insight, action, recommendation, and decision blocks.
7. Package the project as a recruiter-ready analytics repository.

---

## Dashboard Preview

The dashboard includes:

- KPI tiles for total cost, average claim amount, total claims, and YoY change
- Region and claim type filters
- Claim distribution heatmap by region and claim type
- Claim type stacked comparison
- Cost trend over time
- Insight, action, recommendation, and decision panel

---

## Product / Business Insights

- **Property claims are the largest cost driver**, making this the strongest candidate for pricing review and underwriting attention.
- **South has the highest total claim cost**, signaling a need for region-specific risk monitoring.
- YoY claim cost increased by approximately **94.53%**, suggesting cost pressure that should be monitored monthly.
- Severity segmentation helps identify where high-cost claims may be concentrated.

---

## Experimentation Thinking

Although this is a dashboard project, it can support experimentation-style decision making:

| Experiment Idea | Business Question | Success Metric | Guardrail Metric |
|---|---|---|---|
| Pricing adjustment pilot | Does premium adjustment reduce loss pressure? | Lower claim cost ratio | Customer retention |
| Claims triage pilot | Does early review reduce high-cost claims? | Lower average claim amount | Claim resolution time |
| Underwriting rules pilot | Do tighter rules reduce severe claims? | Lower severe-claim share | Policy approval rate |

---

## Recommendations

1. Review pricing for high-cost claim types, especially **Property**.
2. Investigate high-growth and high-cost regions, starting with **South**.
3. Strengthen underwriting rules for high-severity and high-cost segments.
4. Monitor monthly claim-cost trends to detect early cost spikes.
5. Build automated KPI refresh workflows for repeatable executive reporting.

---

## Decision Framework

| Decision Area | Recommended Action |
|---|---|
| Pricing | Adjust premiums for high-cost policy segments |
| Underwriting | Strengthen review rules for severe and high-cost claims |
| Claims Operations | Prioritize early intervention for high-risk claims |
| Executive Monitoring | Use monthly dashboards to track cost trend and YoY movement |

---

## Business Impact

This project demonstrates how insurance claim data can be transformed into an executive decision-support system. The analysis helps identify high-cost claim drivers, prioritize underwriting review, support pricing decisions, and monitor financial exposure across regions and claim types.

---

## Streamlit App

A Streamlit version of the dashboard is included in `app/streamlit_app.py`.

Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## Repo Architecture

```text
insurance-claims-cost-analysis/
├── data/
│   └── claims_cost.csv
├── sql/
│   ├── claims_analysis.sql
│   ├── segmentation_analysis.sql
│   ├── trend_analysis.sql
│   └── risk_analysis.sql
├── notebooks/
│   ├── eda.ipynb
│   ├── business_insights.ipynb
│   └── kpi_analysis.ipynb
├── dashboard/
│   └── tableau_dashboard_placeholder.md
├── screenshots/
│   └── insurance_claims_cost_dashboard.png
├── app/
│   ├── streamlit_app.py
│   ├── components.py
│   └── utils.py
├── docs/
│   ├── business_case.md
│   ├── dashboard_guide.md
│   ├── kpi_definitions.md
│   └── repo_formula_v2.txt
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Automation Awareness

Future versions can automate this workflow using:

- Python scripts for data validation and KPI refresh
- Scheduled SQL jobs for monthly aggregation
- Streamlit Cloud for interactive deployment
- GitHub Actions for quality checks
- Prefect for workflow orchestration when the project becomes more advanced

---

## Future Improvements

- Add loss ratio if premium data becomes available
- Add broker performance analysis
- Add customer risk segmentation
- Add anomaly detection for claim spikes
- Add predictive claim severity model
- Add Tableau packaged workbook when available
