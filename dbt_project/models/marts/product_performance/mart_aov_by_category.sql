with order_categories as (
    select distinct
        o.order_id,
        p.product_type,
        o.total_price,
        o.year,
        o.month_number
    from {{ ref('stg_order_line_items') }} li
    inner join {{ ref('stg_products') }} p on li.product_id = p.product_id
    inner join {{ ref('int_orders_enriched') }} o 
        on li.order_id = o.order_id
        and o.is_cancelled = false
)

select
    product_type,
    year,
    month_number,
    avg(total_price) as avg_order_value,
    count(distinct order_id) as order_count
from order_categories
group by 1, 2, 3