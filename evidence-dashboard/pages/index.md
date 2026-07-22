---
title: SV8 Athletics — Retail Analytics
---

# Retail Analytics Engineering
## A end-to-end analytics pipeline for a simulated DTC apparel brand

Retail companies sit on enormous transactional data but struggle to turn it into decisions. This project builds the analytics foundation that bridges that gap — clean dimensional models, tested pipelines, and business-ready dashboards that answer the questions a growth team, merchandising team, and ops team actually ask.

---

## Key Findings

**Customer Retention**
41% of customers placed a second order — but declining new acquisition rates suggest the brand needs to reinvest in top-of-funnel growth while its loyal core holds. Discount effectiveness is inconsistent across cohorts, with no clear evidence that discounts drive long-term loyalty over one-time purchases.

**Product Performance**
Outerwear drives 30% of total revenue despite representing one of six categories — but the top revenue product (Cascade Windbreaker) carries a below-average satisfaction score of 3.8, representing a retention risk. Revenue is more evenly distributed than the typical 80/20 retail pattern, suggesting no dangerous over-reliance on individual SKUs.

**Fulfillment Experience**
Delivery delay is the single strongest predictor of customer satisfaction in this dataset. Orders delivered within 5 days average a 4.47 rating. Orders delayed beyond 10 days average 1.79 — a 60% drop. Fulfillment SLAs are effectively a retention lever.

---

## Explore

**[→ Customer Retention](/1-customer-retention)**
Acquisition trends, churn rate, lifetime value, and discount effectiveness by cohort and province.

**[→ Product Performance](/2-product-performance)**
Revenue by category, rating vs revenue rank, AOV, and catalogue coverage rate.

**[→ Fulfillment Experience](/3-fulfillment-experience)**
Delivery delay rates, cancellation trends, and satisfaction by delay bucket.

---

## The Pipeline

![DAG](/dag.png)

| Layer | Tool | Purpose |
|---|---|---|
| Data Generation | Python + Faker | Synthetic retail data modeled on Shopify schema |
| Ingestion | dlt | CSV → DuckDB raw schema |
| Storage | DuckDB | Local analytical warehouse |
| Transformation | dbt Core | Staging → Intermediate → Marts |
| Dashboard | Evidence.dev | SQL-first analytics dashboards |

---

## The Data

- **1,000** customers across 10 Canadian provinces
- **2,273** orders over 2 years (2023–2024)
- **5,621** order line items across 60 products in 6 apparel categories
- **900** customer reviews with delivery delay and rating correlation
- **22 dbt models** — 6 staging, 4 intermediate, 12 marts
- **110 data tests** passing across all layers

---

*Built by Shlok Verma · [GitHub](https://github.com/shlokverma) · [Portfolio](https://5hlok.com)*