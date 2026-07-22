with product_ratings as (
    select
        product_id,
        product_name,
        product_type,
        sum(total_revenue) as total_revenue,
        avg(avg_rating) as avg_rating,
        rank() over (
            order by sum(total_revenue) desc
        ) as revenue_rank
    from {{ ref('int_product_metrics') }}
    group by 1, 2, 3
)

select * from product_ratings