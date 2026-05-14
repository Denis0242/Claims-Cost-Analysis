-- Customer Risk Cleaning Logic
-- Use this script as the SQL equivalent of the EDA cleaning workflow.

WITH base AS (
    SELECT
        TRIM(claim_id) AS claim_id,
        CAST(claim_date AS DATE) AS claim_date,
        TRIM(customer_id) AS customer_id,
        INITCAP(TRIM(region)) AS region,
        INITCAP(TRIM(policy_type)) AS policy_type,
        TRIM(customer_age_band) AS customer_age_band,
        CAST(tenure_years AS INTEGER) AS tenure_years,
        CAST(annual_premium AS DECIMAL(12,2)) AS annual_premium,
        INITCAP(TRIM(claim_status)) AS claim_status,
        CAST(claim_amount AS DECIMAL(12,2)) AS claim_amount
    FROM customer_risk
),
deduped AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY claim_id ORDER BY claim_date DESC) AS rn
    FROM base
),
cleaned AS (
    SELECT *,
           claim_amount / NULLIF(annual_premium, 0) AS loss_ratio,
           DATE_TRUNC('month', claim_date) AS claim_month
    FROM deduped
    WHERE rn = 1
      AND claim_id IS NOT NULL
      AND customer_id IS NOT NULL
      AND claim_date IS NOT NULL
      AND claim_amount >= 0
      AND annual_premium >= 0
)
SELECT * FROM cleaned;
