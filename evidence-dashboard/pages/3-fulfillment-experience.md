---
title: Fulfillment Experience
queries:
  hide: true
---

Understanding how delivery performance impacts customer satisfaction at SV8 Athletics.

---

## The Headlines

```sql fulfillment_headline
select
    round(avg(delayed_order_rate), 1) as avg_delayed_order_rate,
    round(avg(avg_delay_days), 1) as avg_delay_days,
    round(avg(cancellation_rate), 1) as avg_cancellation_rate
from marts.mart_delivery_performance
```

<Grid cols=3>
<BigValue 
    data={fulfillment_headline}
    value=avg_delayed_order_rate
    title="Avg Delayed Order Rate (%)"
/>
<BigValue 
    data={fulfillment_headline}
    value=avg_delay_days
    title="Avg Delivery Delay (Days)"
/>
<BigValue 
    data={fulfillment_headline}
    value=avg_cancellation_rate
    title="Avg Cancellation Rate (%)"
/>
</Grid>

---

## Delivery Performance Over Time

Delayed order rate and cancellation rate are tracked monthly to identify fulfillment trends and operational issues.

```sql delivery
select * from marts.mart_delivery_performance
order by month
```

<Grid cols=2>
<LineChart 
    data={delivery}
    x=month
    y=delayed_order_rate
    title="Delayed Order Rate by Month (%)"
    xSort=sort_key
/>
<LineChart 
    data={delivery}
    x=month
    y=cancellation_rate
    title="Cancellation Rate by Month (%)"
    xSort=sort_key
/>
</Grid>

<LineChart 
    data={delivery}
    x=month
    y=avg_delay_days
    title="Average Delivery Delay by Month (Days)"
    xSort=sort_key
/>
---

## The Core Finding — Delivery Delay Drives Dissatisfaction

This is the strongest signal in the dataset. Orders delivered within 5 days average a 4.47 rating. Orders delayed beyond 10 days average just 1.79 — a 60% drop in satisfaction.

```sql ratings_by_delay
select
    delay_bucket,
    round(avg(avg_rating), 2) as avg_rating,
    sum(review_count) as total_reviews
from marts.mart_rating_by_delay
group by delay_bucket
order by avg_rating desc
```

<BarChart 
    data={ratings_by_delay}
    x=delay_bucket
    y=avg_rating
    title="Average Rating by Delivery Delay Bucket"
    yMin=0
    yMax=5
/>

> **Key finding:** Delivery delay is the single strongest predictor of customer satisfaction in this dataset. Orders delayed beyond 10 days receive 1-star or 2-star reviews 80% of the time. Fulfillment SLAs are effectively a retention lever — faster delivery directly protects repeat purchase rates.

---

## Review Volume by Delay Bucket

```sql review_volume
select
    delay_bucket,
    sum(review_count) as total_reviews
from marts.mart_rating_by_delay
group by delay_bucket
order by total_reviews desc
```

<BarChart 
    data={review_volume}
    x=delay_bucket
    y=total_reviews
    title="Review Volume by Delay Bucket"
/>

> The majority of reviews come from fast deliveries — which is expected given 70% of orders in the dataset were generated with 0-5 day delivery times. Long delay reviews are fewer but consistently negative.