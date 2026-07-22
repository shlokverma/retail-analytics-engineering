with products as (
    select * from {{ ref('stg_products') }}
),

order_line_items as (
    select * from {{ ref('stg_order_line_items') }}
),

orders as (
    select * from {{ ref('int_orders_enriched') }}
),

reviews as (
    select * from {{ ref('stg_reviews') }}
),

product_metrics as (
    select
        p.product_id,
        p.product_name,
        p.product_type,
        o.year,
        o.month_number,
        sum(li.line_subtotal) as total_revenue,
        sum(li.quantity) as qty_sold,
        count(distinct li.order_id) as order_count,
        avg(r.rating) as avg_rating
    from order_line_items li
    inner join orders o
        on li.order_id = o.order_id
        and o.is_cancelled = false
    inner join products p
        on li.product_id = p.product_id
    left join reviews r
        on li.product_id = r.product_id
        and date_trunc('month', r.review_date) = date_trunc('month', o.order_date)
    group by 1, 2, 3, 4, 5
)

select * from product_metrics