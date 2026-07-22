with source as (
    select * from {{ source('raw', 'customers') }}
),

renamed as (
    select
        customer_id,
        trim(first_name) as first_name  ,
        trim(last_name) as last_name,
        trim(email) as email,
        created_at::date as created_at,
        trim(city) as city,
        trim(province) as province,
        coalesce(trim(country), 'Canada') as country,
        accepts_marketing::boolean as accepts_marketing
    from source
)

select * from renamed 