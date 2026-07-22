with source as (
    select * from {{ source('raw', 'date_dimension') }}
),

renamed as (
    select
        date_id,
        full_date::date as full_date,
        trim(day_of_week) as day_of_week,
        day_of_month::int as day_of_month,
        month::int as month_number,
        trim(month_name) as month_name,
        quarter::int as quarter,
        year::int as year,
        is_weekend::boolean as is_weekend
    from source
)

select * from renamed 