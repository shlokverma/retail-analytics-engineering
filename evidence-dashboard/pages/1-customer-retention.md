---
title: Customer Retention
queries:
  hide: true
---

Understanding how SV8 Athletics acquires and retains customers over time.

---

## The Headlines

```sql headline_metrics
select * from marts.mart_retention_summary
```

<Grid cols=3>
<BigValue 
    data={headline_metrics}
    value=total_customers
    title="Total Customers"
/>
<BigValue 
    data={headline_metrics}
    value=repeat_purchase_rate
    title="Repeat Purchase Rate (%)"
    fmt='0.0'
/>
<BigValue 
    data={headline_metrics}
    value=churn_rate
    title="Churn Rate (%)"
    fmt='0.0'
/>
</Grid>

---

## Acquisition vs Retention

New customer acquisition declined through 2023–2024, while repeat purchase rates held steady — suggesting the brand's retained customer base is increasingly loyal.

```sql new_customers
select 
    acquisition_month,
    sum(new_customers) as new_customers
from marts.mart_customer_acquisition
group by acquisition_month
order by acquisition_month
```

```sql repeat_purchase
select 
    acquisition_month,
    avg(repeat_purchase_rate) as repeat_purchase_rate
from marts.mart_repeat_purchase
where province in ('Ontario', 'Quebec', 'British Columbia', 'Alberta')
group by acquisition_month
order by acquisition_month
```

<Grid cols=2>
<LineChart 
    data={new_customers}
    x=acquisition_month
    y=new_customers
    title="New Customers by Month"
/>
<LineChart 
    data={repeat_purchase}
    x=acquisition_month
    y=repeat_purchase_rate
    title="Repeat Purchase Rate by Month"
/>
</Grid>

---

## Churn Analysis

Churn rates remain high across all cohorts — reflecting that most customers are one-time purchasers. Recent cohorts show lower churn due to data cutoff at December 2024, not improved retention.

```sql churn
select 
    acquisition_month,
    sum(churned_customers) * 100.0 / sum(total_customers) as churn_rate
from marts.mart_churn
group by acquisition_month
order by acquisition_month
```

```sql days_since_order
select 
    province,
    avg(avg_days_since_last_order) as avg_days
from marts.mart_churn
group by province
order by avg_days desc
```

<Grid cols=2>
<LineChart 
    data={churn}
    x=acquisition_month
    y=churn_rate
    title="Churn Rate by Cohort Month"
/>
<BarChart 
    data={days_since_order}
    x=province
    y=avg_days
    title="Avg Days Since Last Order by Province"
    swapXY=true
/>
</Grid>

---

## Customer Lifetime Value

Average LTV varies across cohorts without a clear trend — consistent with synthetic data. In production, earlier cohorts would show higher LTV given more time to purchase.

```sql ltv
select
    cohort_month,
    avg(lifetime_value) as avg_ltv
from marts.mart_customer_ltv
group by cohort_month
order by cohort_month
```

<LineChart 
    data={ltv}
    x=cohort_month
    y=avg_ltv
    title="Average Customer LTV by Cohort Month"
/>

---

## Discount Effectiveness

Discount impact on repeat purchase rate is inconsistent across cohorts — suggesting discounts attract price-sensitive buyers rather than building long-term loyalty.

```sql discount
select
    cohort_month,
    avg(discount_repeat_rate) as discount_repeat_rate,
    avg(non_discount_repeat_rate) as non_discount_repeat_rate
from marts.mart_discount_effectiveness
where province in ('Ontario', 'Quebec', 'British Columbia', 'Alberta')
group by cohort_month
order by cohort_month
```

<LineChart 
    data={discount}
    x=cohort_month
    y={['discount_repeat_rate', 'non_discount_repeat_rate']}
    title="Discount vs Non-Discount Repeat Purchase Rate"
/>