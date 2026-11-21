# Power BI implementation guide

## Connect
Power BI Desktop → Get Data → PostgreSQL database. Server `localhost:5432`, database `salespulse`. Import `analytics.vw_sales_enriched` and aggregate views.

## Recommended star model
Import warehouse fact_sales and dimensions. Create one-to-many, single-direction relationships:
- dim_customer.customer_id → fact_sales.customer_id
- dim_product.product_id → fact_sales.product_id
- dim_region.region_id → fact_sales.region_id
- dim_sales_rep.sales_rep_id → fact_sales.sales_rep_id

## DAX measures (adapt table names to your imported model)
```dax
Net Revenue = CALCULATE(SUM(fact_sales[net_sales]), fact_sales[status] = "Completed")
Total Profit = CALCULATE(SUM(fact_sales[profit]), fact_sales[status] = "Completed")
Completed Orders = CALCULATE(DISTINCTCOUNT(fact_sales[order_id]), fact_sales[status] = "Completed")
Units Sold = CALCULATE(SUM(fact_sales[quantity]), fact_sales[status] = "Completed")
Average Order Value = DIVIDE([Net Revenue], [Completed Orders])
Profit Margin = DIVIDE([Total Profit], [Net Revenue])
```

## Page 1 — Executive Overview
KPI cards: Net Revenue, Total Profit, Completed Orders, AOV, Margin. Add monthly revenue line chart, category revenue/profit columns, channel share donut, date/region/category slicers.

## Page 2 — Regional Performance
Bar chart by region/city, matrix region × month, profit-margin KPI, region and date slicers.

## Page 3 — Product & Sales
Top 10 products by revenue, category/subcategory treemap, product revenue vs profit scatter, detailed product table.

## Page 4 — Customer Analytics
Revenue by segment, top customer table, repeat customer classification, customer city and segment slicers.

## Quality checks before screenshots
- Compare Power BI KPI totals with `SELECT * FROM analytics.vw_executive_kpis`.
- Verify order counts use DISTINCTCOUNT because each order may have multiple item rows.
- Format currency consistently; label date ranges; avoid clutter and 3D charts.
- Capture your own screenshots in `docs/screenshots/`.
