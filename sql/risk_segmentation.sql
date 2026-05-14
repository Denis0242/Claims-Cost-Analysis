-- Risk Segmentation Query
-- Default thresholds match the Streamlit app / Tableau view:
-- claim_threshold = 4, loss_threshold = 15000

WITH customer_summary AS (
    SELECT
        customer_id,
        MIN(region) AS region,
        MIN(policy_type) AS policy_type,
        MIN(customer_age_band) AS customer_age_band,
        COUNT(DISTINCT claim_id) AS claims_count,
        SUM(claim_amount) AS total_loss,
        AVG(claim_amount) AS avg_loss,
        AVG(annual_premium) AS avg_annual_premium
    FROM cleaned_customer_risk
    GROUP BY customer_id
)
SELECT *,
       CASE
           WHEN claims_count >= 4 OR total_loss >= 15000 THEN 'High-risk'
           WHEN claims_count >= 2 OR total_loss >= 7500 THEN 'Medium-risk'
           ELSE 'Low-risk'
       END AS risk_category
FROM customer_summary;
