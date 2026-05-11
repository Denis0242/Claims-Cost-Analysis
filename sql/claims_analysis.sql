-- Claims KPI Summary
SELECT
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount,
    MIN(claim_date) AS first_claim_date,
    MAX(claim_date) AS last_claim_date
FROM claims_cost;

-- Claim cost by region
SELECT
    region,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY region
ORDER BY total_claim_cost DESC;

-- Claim cost by claim type
SELECT
    claim_type,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY claim_type
ORDER BY total_claim_cost DESC;
