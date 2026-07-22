with products_sold as (
    select
        date_trunc('month', make_date(year::int, month_number::int, 1)) as month,
        count(distinct product_id) as products_with_sales
    from {{ ref('int_product_metrics') }}
    group by 1
),

total_products as (
    select count(distinct product_id) as total_catalogue_size
    from {{ ref('stg_products') }}
),

final as (
    select
        ps.month,
        ps.products_with_sales,
        tp.total_catalogue_size,
        ps.products_with_sales / tp.total_catalogue_size * 100 as coverage_rate
    from products_sold ps
    cross join total_products tp
)

select * from final