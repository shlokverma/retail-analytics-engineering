with product_revenue as (
    select
        product_id,
        product_name,
        product_type,
        year,
        month_number,
        total_revenue,
        rank() over (
            partition by year, month_number
            order by total_revenue desc
        ) as revenue_rank,
        total_revenue / sum(total_revenue) over (
            partition by year, month_number
        ) * 100 as revenue_share_pct
    from {{ ref('int_product_metrics') }}
),

final as (
    select
        *,
        sum(revenue_share_pct) over (
            partition by year, month_number
            order by revenue_rank
            rows between unbounded preceding and current row
        ) as cumulative_revenue_pct
    from product_revenue
)

select * from final