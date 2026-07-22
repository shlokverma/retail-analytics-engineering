select
    date_trunc('month', first_order_date) as acquisition_month,
    extract(year from first_order_date) as year,
    province,
    avg(days_since_last_order) as avg_days_since_last_order,
    count(distinct case when days_since_last_order > 90 then customer_id end) as churned_customers,
    count(distinct customer_id) as total_customers,
    count(distinct case when days_since_last_order > 90 then customer_id end) * 100.0
    / nullif(count(distinct customer_id), 0) as churn_rate
from {{ ref('int_customer_orders') }}
where first_order_date is not null
group by 1, 2, 3