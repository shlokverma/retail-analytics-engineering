with source as (
    select * from {{ source('raw', 'products') }}
),

renamed as (
    select
        product_id,
        trim(title) as product_name,
        trim(product_type) as product_type,
        trim(vendor_country) as vendor_country,
        price::decimal(10,2) as price
    from source
)

select * from renamed 