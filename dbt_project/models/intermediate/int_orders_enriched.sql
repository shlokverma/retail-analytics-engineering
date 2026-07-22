with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

date_dim as (
    select * from {{ ref('stg_date_dimension') }}
),

enriched as (
    select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.discount_code,
    o.discount_used,
    o.discount_amount,
    o.subtotal,
    o.total_price,
    o.status = 'cancelled' as is_cancelled,
    o.status = 'refunded' as is_refunded,
    o.cancelled_at,
    c.province,
    c.accepts_marketing,
    d.year,
    d.quarter,
    d.month_number,
    d.is_weekend,
    d.day_of_week,
    case
    when o.status = 'fulfilled' then o.total_price
    when o.status = 'refunded' then -o.total_price
    when o.status = 'cancelled' then 0
    end as recognized_revenue
    from orders o
    left join customers c on o.customer_id = c.customer_id
    left join date_dim d on o.order_date = d.full_date
)

select * from enriched