with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        created_at::date as order_date,
        trim(status) as status,
        trim(discount_code) as discount_code,
        discount_code is not null as discount_used,
        discount_amount::decimal(10,2) as discount_amount,
        subtotal::decimal(10,2) as subtotal,
        total_price::decimal(10,2) as total_price,
        cancelled_at::date as cancelled_at
    from source
)

select * from renamed 