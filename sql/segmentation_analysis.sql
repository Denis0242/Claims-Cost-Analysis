-- Region x Claim Type Cost Matrix
SELECT
    region,
    claim_type,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY region, claim_type
ORDER BY region, total_claim_cost DESC;

-- Claim status segmentation
SELECT
    claim_status,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount
FROM claims_cost
GROUP BY claim_status
ORDER BY total_claim_cost DESC;
