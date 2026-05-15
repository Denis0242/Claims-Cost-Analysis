-- Insurance Claims Cost Analysis SQL

-- 1. KPI Summary
SELECT
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount,
    COUNT(DISTINCT claim_id) AS total_claims,
    COUNT(DISTINCT policy_id) AS total_policies,
    COUNT(DISTINCT customer_id) AS total_customers
FROM claims_cost;

-- 2. Monthly Cost Trend
SELECT
    DATE_TRUNC('month', claim_date) AS claim_month,
    SUM(claim_amount) AS monthly_claim_cost,
    COUNT(DISTINCT claim_id) AS monthly_claims,
    AVG(claim_amount) AS avg_monthly_claim_amount
FROM claims_cost
GROUP BY 1
ORDER BY 1;

-- 3. Cost by Region
SELECT
    region,
    SUM(claim_amount) AS total_claim_cost,
    COUNT(DISTINCT claim_id) AS total_claims,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY region
ORDER BY total_claim_cost DESC;

-- 4. Cost by Claim Type
SELECT
    claim_type,
    SUM(claim_amount) AS total_claim_cost,
    COUNT(DISTINCT claim_id) AS total_claims,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY claim_type
ORDER BY total_claim_cost DESC;

-- 5. Severity Analysis
SELECT
    severity,
    SUM(claim_amount) AS total_claim_cost,
    COUNT(DISTINCT claim_id) AS total_claims,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY severity
ORDER BY total_claim_cost DESC;

-- 6. Year-over-Year Claim Cost
WITH yearly AS (
    SELECT claim_year, SUM(claim_amount) AS total_claim_cost
    FROM claims_cost
    GROUP BY claim_year
)
SELECT
    claim_year,
    total_claim_cost,
    LAG(total_claim_cost) OVER (ORDER BY claim_year) AS prior_year_cost,
    (total_claim_cost - LAG(total_claim_cost) OVER (ORDER BY claim_year)) /
        NULLIF(LAG(total_claim_cost) OVER (ORDER BY claim_year), 0) AS yoy_change
FROM yearly
ORDER BY claim_year;

-- 7. High-Cost Claim Detail
SELECT *
FROM claims_cost
WHERE high_cost_flag = 1
ORDER BY claim_amount DESC;

-- 8. Broker Exposure
SELECT
    broker_id,
    SUM(claim_amount) AS broker_claim_cost,
    COUNT(DISTINCT claim_id) AS broker_claim_count,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY broker_id
ORDER BY broker_claim_cost DESC;
