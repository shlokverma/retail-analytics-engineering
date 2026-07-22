select
    date_trunc('month', first_order_date) as acquisition_month,
    extract(year from first_order_date) as year,
    province,
    count(distinct case when total_orders >= 2 then customer_id end) as repeat_customers,
    count(distinct case when total_orders >= 1 then customer_id end) as total_customers,
    avg(days_to_second_order) as avg_days_to_second_order,
    count(distinct case when total_orders >= 2 then customer_id end) * 100.0 
    / nullif(count(distinct case when total_orders >= 1 then customer_id end), 0) as repeat_purchase_rate
from {{ ref('int_customer_orders') }}
where first_order_date is not null
group by 1, 2, 3