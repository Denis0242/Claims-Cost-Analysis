# EDA & Data Cleaning — Insurance Claims Cost Analysis

## 1. Import Libraries
```python
import pandas as pd
import numpy as np
```

## 2. Load Dataset
```python
df = pd.read_csv("data/claims_cost.csv")
df.head()
```

## 3. Dataset Shape
```python
df.shape
```

## 4. Data Types
```python
df.info()
```

## 5. Descriptive Statistics
```python
df.describe()
```

## 6. Column Standardization
```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)
```

## 7. Missing Value Check
```python
df.isnull().sum()
```

## 8. Duplicate Check
```python
df.duplicated().sum()
df = df.drop_duplicates()
```

## 9. Date Conversion
```python
df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
df["claim_month_name"] = df["claim_date"].dt.strftime("%b")
df["claim_quarter"] = "Q" + df["claim_date"].dt.quarter.astype(str)
```

## 10. Numeric Validation
```python
df["claim_amount"] = pd.to_numeric(df["claim_amount"], errors="coerce")
df[df["claim_amount"] < 0]
```

## 11. Categorical Validation
```python
for col in ["region", "claim_type", "severity", "claim_status"]:
    print(col)
    print(df[col].value_counts(dropna=False))
```

## 12. Outlier Detection
```python
q1 = df["claim_amount"].quantile(0.25)
q3 = df["claim_amount"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
outliers = df[df["claim_amount"] > upper_bound]
outliers.head()
```

## 13. Feature Engineering
```python
df["high_cost_flag"] = (df["claim_amount"] >= df["claim_amount"].quantile(0.75)).astype(int)
df["cost_band"] = pd.cut(
    df["claim_amount"],
    bins=[-1, 1000, 3000, 6000, 10000, float("inf")],
    labels=["Very Low", "Low", "Medium", "High", "Extreme"]
)
```

## 14. KPI Validation
```python
total_claim_cost = df["claim_amount"].sum()
avg_claim_amount = df["claim_amount"].mean()
total_claims = df["claim_id"].nunique()
print(total_claim_cost, avg_claim_amount, total_claims)
```

## 15. Export Cleaned Dataset
```python
df.to_csv("data/claims_cost.csv", index=False)
```

## Final EDA Summary
The dataset is clean enough for dashboarding after date conversion, duplicate review, missing value checks, categorical validation, and cost-band feature engineering. The cleaned data supports Tableau, SQL analysis, and Streamlit dashboard recreation.
