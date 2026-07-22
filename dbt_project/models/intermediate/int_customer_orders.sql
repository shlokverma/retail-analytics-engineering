with customers as (
    select * from {{ ref('stg_customers') }}
),

    orders as (
        select * from {{ ref('int_orders_enriched') }}
    ),

orders_ranked as (
    select
        *,
        row_number() over (
            partition by customer_id 
            order by order_date asc
        ) as order_rank
    from orders
    where is_cancelled = false
),

customer_orders as (
    select
        c.customer_id,
        c.province,
        c.accepts_marketing,
        c.created_at as customer_created_at,
        coalesce(count(o.order_id), 0) as total_orders,
        coalesce(sum(o.recognized_revenue), 0) as total_revenue,
        min(o.order_date) as first_order_date,
        min(case when o.order_rank = 2 then o.order_date end) as second_order_date,
        datediff('day', max(o.order_date), date '2024-12-31') as days_since_last_order,
        datediff('day', 
            min(o.order_date), 
            min(case when o.order_rank = 2 then o.order_date end)
        ) as days_to_second_order
    from customers c
    left join orders_ranked o on c.customer_id = o.customer_id
    group by 1, 2, 3, 4
)

select * from customer_orders