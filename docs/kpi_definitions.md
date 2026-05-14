# KPI Definitions

## Total Customers
Unique count of customer_id after filters.

## Average Loss per Customer
Average of each customer's total claim loss.

## Total Loss
Sum of customer-level total_loss after filters.

## High Risk Customer %
High-risk customers divided by all selected customers.

## Risk Category
Default Streamlit logic:
- High-risk: claims_count >= claim_threshold OR total_loss >= loss_threshold
- Medium-risk: claims_count >= half of claim_threshold OR total_loss >= 50% of loss_threshold
- Low-risk: all other customers

## Loss Ratio
claim_amount / annual_premium at claim level; total_loss / average annual premium at customer level.
