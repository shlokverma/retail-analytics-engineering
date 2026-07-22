with source as (
    select * from {{ source('raw', 'reviews') }}
),

renamed as (
    select
        review_id,
        order_id,
        customer_id,
        product_id,
        rating::int as rating,
        trim(review_text) as review_text,
        delivery_delay_days::int as delivery_delay_days,
        created_at::date as review_date
    from source
)

select * from renamed 