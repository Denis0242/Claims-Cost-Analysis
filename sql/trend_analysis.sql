-- Monthly claim cost trend
SELECT
    claim_year,
    claim_month,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY claim_year, claim_month
ORDER BY claim_year, claim_month;

-- YoY claim cost change
WITH yearly AS (
    SELECT claim_year, SUM(claim_amount) AS total_claim_cost
    FROM claims_cost
    GROUP BY claim_year
)
SELECT
    claim_year,
    total_claim_cost,
    LAG(total_claim_cost) OVER (ORDER BY claim_year) AS prior_year_cost,
    (total_claim_cost - LAG(total_claim_cost) OVER (ORDER BY claim_year))
        / NULLIF(LAG(total_claim_cost) OVER (ORDER BY claim_year), 0) AS yoy_pct_change
FROM yearly;
