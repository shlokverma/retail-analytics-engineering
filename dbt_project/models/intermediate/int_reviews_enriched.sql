with reviews as (
    select * from {{ ref('stg_reviews') }}
),

orders as (
    select * from {{ ref('int_orders_enriched') }}
),

reviews_enriched as (
    select
        r.review_id,
        r.order_id,
        r.customer_id,
        r.product_id,
        r.rating,
        r.review_text,
        r.delivery_delay_days,
        r.review_date,
        case
            when r.delivery_delay_days <= 5 then 'fast'
            when r.delivery_delay_days <= 10 then 'mild'
            else 'long'
        end as delay_bucket,
        o.month_number,
        o.year,
        o.province,
        o.is_cancelled
    from reviews r
    left join orders o on r.order_id = o.order_id
)

select * from reviews_enriched