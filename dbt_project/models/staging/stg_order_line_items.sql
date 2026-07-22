with source as (
    select * from {{ source('raw', 'order_line_items') }}
),

renamed as (
    select
        line_item_id,
        order_id,
        product_id,
        quantity::int as quantity,
        unit_price::decimal(10,2) as unit_price,
        line_subtotal::decimal(10,2) as line_subtotal
    from source
)

select * from renamed 