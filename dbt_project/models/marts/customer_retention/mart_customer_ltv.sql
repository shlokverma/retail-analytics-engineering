select
    province,
    date_trunc('month', first_order_date) as cohort_month,
    extract(year from first_order_date) as year,
    avg(total_revenue) as lifetime_value,
    count(distinct customer_id) as customer_count
from {{ ref('int_customer_orders') }}
where first_order_date is not null
group by 1, 2, 3    