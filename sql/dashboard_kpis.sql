-- Executive Dashboard KPIs

SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(total_loss) AS avg_loss_per_customer,
    SUM(total_loss) AS total_loss,
    100.0 * SUM(CASE WHEN risk_category = 'High-risk' THEN 1 ELSE 0 END) / COUNT(*) AS high_risk_customer_pct
FROM customer_risk_segments;

SELECT risk_category, COUNT(*) AS customers, SUM(total_loss) AS total_loss
FROM customer_risk_segments
GROUP BY risk_category
ORDER BY total_loss DESC;

SELECT customer_age_band, COUNT(DISTINCT claim_id) AS claims
FROM cleaned_customer_risk
GROUP BY customer_age_band
ORDER BY customer_age_band;
