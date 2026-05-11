-- Severity risk analysis
SELECT
    severity,
    COUNT(DISTINCT claim_id) AS total_claims,
    SUM(claim_amount) AS total_claim_cost,
    AVG(claim_amount) AS avg_claim_amount,
    MAX(claim_amount) AS max_claim_amount
FROM claims_cost
GROUP BY severity
ORDER BY total_claim_cost DESC;

-- High-cost claims for underwriting review
SELECT *
FROM claims_cost
WHERE claim_amount >= (
    SELECT AVG(claim_amount) + 2 * STDDEV(claim_amount)
    FROM claims_cost
)
ORDER BY claim_amount DESC;
