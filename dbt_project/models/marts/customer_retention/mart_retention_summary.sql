-- mart_retention_summary.sql
select
    count(distinct customer_id) as total_customers,
    count(distinct case when total_orders >= 2 then customer_id end) * 100.0 
    / count(distinct customer_id) as repeat_purchase_rate,
    count(distinct case when days_since_last_order > 90 then customer_id end) * 100.0 
    / count(distinct customer_id) as churn_rate
from {{ ref('int_customer_orders') }}
where first_order_date is not null