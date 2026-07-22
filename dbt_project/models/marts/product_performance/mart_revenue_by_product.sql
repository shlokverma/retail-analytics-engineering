select
    product_id,
    product_name,
    product_type,
    year,
    month_number,
    sum(total_revenue) as total_revenue,
    sum(qty_sold) as qty_sold,
    sum(order_count) as order_count,
    avg(avg_rating) as avg_rating
from {{ ref('int_product_metrics') }}
group by 1, 2, 3, 4, 5