with customer_orders as (
    select * from {{ ref('int_customer_orders') }}
),

first_orders as (
    select
        o.customer_id,
        o.discount_used
    from {{ ref('int_orders_enriched') }} o
    inner join customer_orders c
        on o.customer_id = c.customer_id
        and o.order_date = c.first_order_date
),

discount_effectiveness as (
    select
        date_trunc('month', c.first_order_date) as cohort_month,
        extract(year from c.first_order_date) as year,
        c.province,
        -- repeat rate for customers who used discount on first order
        count(distinct case when f.discount_used = true and c.total_orders >= 2 then c.customer_id end) * 100.0
        / nullif(count(distinct case when f.discount_used = true then c.customer_id end), 0) as discount_repeat_rate,

        -- repeat rate for customers who did NOT use discount on first order
        count(distinct case when f.discount_used = false and c.total_orders >= 2 then c.customer_id end) * 100.0
        / nullif(count(distinct case when f.discount_used = false then c.customer_id end), 0) as non_discount_repeat_rate
    from customer_orders c
    left join first_orders f on c.customer_id = f.customer_id
    where c.first_order_date is not null
    group by 1, 2, 3
)

select * from discount_effectiveness