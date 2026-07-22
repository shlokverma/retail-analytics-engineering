select
    date_trunc('month', first_order_date) as acquisition_month,
    extract(year from first_order_date) as year,
    province,
    COUNT(DISTINCT customer_id) as new_customers
from {{ ref('int_customer_orders') }}
where first_order_date is not null
group by 1, 2, 3