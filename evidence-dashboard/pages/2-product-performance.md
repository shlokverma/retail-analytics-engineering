---
title: Product Performance
---

Understanding which products and categories drive revenue, satisfaction, and catalogue breadth for SV8 Athletics.

---

## The Headlines

```sql product_headline
select
    round(sum(total_revenue), 0) as total_revenue,
    sum(qty_sold) as total_units_sold,
    round(avg(avg_rating), 2) as overall_avg_rating
from marts.mart_revenue_by_product
```

<Grid cols=3>
<BigValue 
    data={product_headline}
    value=total_revenue
    title="Total Revenue (CAD)"
    fmt='$#,##0'
/>
<BigValue 
    data={product_headline}
    value=total_units_sold
    title="Total Units Sold"
/>
<BigValue 
    data={product_headline}
    value=overall_avg_rating
    title="Overall Avg Rating"
/>
</Grid>

---

## Revenue by Category

Outerwear dominates revenue driven by higher price points ($150-$400), while Accessories trail significantly despite similar unit volumes. This suggests a pricing opportunity in lower-ASP categories.

```sql revenue_by_category
select
    product_type,
    sum(total_revenue) as total_revenue
from marts.mart_revenue_by_product
group by product_type
order by total_revenue desc
```

```sql aov
select
    product_type,
    round(avg(avg_order_value), 2) as avg_order_value
from marts.mart_aov_by_category
group by product_type
order by avg_order_value desc
```

<Grid cols=2>
<BarChart 
    data={revenue_by_category}
    x=product_type
    y=total_revenue
    title="Total Revenue by Category (CAD)"
    fmt='$#,##0'
/>
<BarChart 
    data={aov}
    x=product_type
    y=avg_order_value
    title="Average Order Value by Category (CAD)"
    swapXY=true
/>
</Grid>

---

## Revenue Concentration

Revenue is relatively evenly distributed across the catalogue — the top 10 products account for ~35% of total revenue, with no single product dominating. This is atypical of real retail where 80/20 concentration is common, reflecting the uniform distribution of synthetic data.

```sql concentration
select
    product_name,
    product_type,
    total_revenue,
    revenue_rank,
    round(total_revenue / total_all_revenue, 3) as revenue_share_pct,
    round(sum(total_revenue / total_all_revenue) over (order by revenue_rank rows between unbounded preceding and current row), 3) as cumulative_revenue_pct
from (
    select
        product_name,
        product_type,
        total_revenue,
        revenue_rank,
        sum(total_revenue) over () as total_all_revenue
    from marts.mart_product_ratings
)
order by revenue_rank
limit 20
```

<DataTable 
    data={concentration}
    rows=10
/>

---

## Rating vs Revenue Rank

High revenue does not always correlate with high satisfaction. The Cascade Windbreaker — the top revenue product — has a below-average rating of 3.8, representing a retention risk. The Tundra Parka ranks 8th in revenue but has the highest satisfaction score at 4.9.

```sql ratings
select
    product_name,
    product_type,
    total_revenue,
    round(avg_rating, 2) as avg_rating,
    revenue_rank
from marts.mart_product_ratings
order by revenue_rank
```

<ScatterPlot
    data={ratings}
    x=revenue_rank
    y=avg_rating
    series=product_type
    title="Avg Rating vs Revenue Rank — lower rank = higher revenue"
/>

> **Key finding:** Products ranked 1-10 by revenue show no consistent satisfaction advantage over lower-ranked products — suggesting sales volume is driven by price and availability rather than customer satisfaction.

---

## Catalogue Coverage Rate

Coverage remains consistently high at 96-100%, meaning nearly all products sell in every month. In production retail data, seasonal variation would cause significant dips — particularly for Outerwear in summer months.

```sql coverage
select * from marts.mart_catalogue_coverage
order by month
```

<LineChart 
    data={coverage}
    x=month
    y=coverage_rate
    title="Catalogue Coverage Rate by Month (%)"
    yMin=80
    xSort=sort_key
/>