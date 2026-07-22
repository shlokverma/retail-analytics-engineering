with delivery_metrics as (
    select
        date_trunc('month', make_date(year::int, month_number::int, 1)) as month,
        count(distinct order_id) as total_reviewed_orders,
        count(distinct case when delivery_delay_days > 5 then order_id end) as delayed_orders,
        avg(delivery_delay_days) as avg_delay_days,
        count(distinct case when delivery_delay_days > 5 then order_id end) * 100.0
        / nullif(count(distinct order_id), 0) as delayed_order_rate
    from {{ ref('int_reviews_enriched') }}
    group by 1
),

cancellation_metrics as (
    select
        date_trunc('month', make_date(year::int, month_number::int, 1)) as month,
        count(distinct order_id) as total_orders,
        count(distinct case when is_cancelled = true then order_id end) as cancelled_orders,
        count(distinct case when is_cancelled = true then order_id end) * 100.0
        / nullif(count(distinct order_id), 0) as cancellation_rate
    from {{ ref('int_orders_enriched') }}
    group by 1
),

final as (
    select
        d.month,
        d.total_reviewed_orders,
        d.delayed_orders,
        d.avg_delay_days,
        d.delayed_order_rate,
        c.total_orders,
        c.cancelled_orders,
        c.cancellation_rate
    from delivery_metrics d
    left join cancellation_metrics c
        on d.month = c.month
)

select * from final