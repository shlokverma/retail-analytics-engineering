    with ratings_by_delay as (
    select
        delay_bucket,
        year,
        month_number,
        avg(rating) as avg_rating,
        count(distinct review_id) as review_count
    from {{ ref('int_reviews_enriched') }}
    group by 1, 2, 3
)

select * from ratings_by_delay