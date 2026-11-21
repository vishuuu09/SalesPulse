CREATE OR REPLACE VIEW analytics.vw_sales_enriched AS
SELECT f.*,c.customer_name,c.segment,c.city AS customer_city,p.product_name,p.category,p.subcategory,
       r.region_name,r.city AS sales_city,s.sales_rep_name,s.team AS sales_team,
       f.profit/NULLIF(f.net_sales,0) AS profit_margin
FROM warehouse.fact_sales f
JOIN warehouse.dim_customer c USING(customer_id)
JOIN warehouse.dim_product p USING(product_id)
JOIN warehouse.dim_region r USING(region_id)
JOIN warehouse.dim_sales_rep s USING(sales_rep_id);

CREATE OR REPLACE VIEW analytics.vw_executive_kpis AS
SELECT COUNT(DISTINCT order_id) FILTER(WHERE status='Completed') AS completed_orders,
       SUM(net_sales) FILTER(WHERE status='Completed') AS net_revenue,
       SUM(profit) FILTER(WHERE status='Completed') AS total_profit,
       SUM(quantity) FILTER(WHERE status='Completed') AS units_sold,
       SUM(net_sales) FILTER(WHERE status='Completed')/
         NULLIF(COUNT(DISTINCT order_id) FILTER(WHERE status='Completed'),0) AS average_order_value,
       SUM(profit) FILTER(WHERE status='Completed')/
         NULLIF(SUM(net_sales) FILTER(WHERE status='Completed'),0) AS profit_margin
FROM analytics.vw_sales_enriched;

CREATE OR REPLACE VIEW analytics.vw_monthly_sales AS
SELECT date_trunc('month',order_date)::date AS month,
       SUM(net_sales) FILTER(WHERE status='Completed') AS revenue,
       SUM(profit) FILTER(WHERE status='Completed') AS profit,
       COUNT(DISTINCT order_id) FILTER(WHERE status='Completed') AS orders
FROM analytics.vw_sales_enriched GROUP BY 1;

CREATE OR REPLACE VIEW analytics.vw_region_performance AS
SELECT region_name,sales_city,SUM(net_sales) FILTER(WHERE status='Completed') AS revenue,
       SUM(profit) FILTER(WHERE status='Completed') AS profit,
       COUNT(DISTINCT order_id) FILTER(WHERE status='Completed') AS orders
FROM analytics.vw_sales_enriched GROUP BY 1,2;

CREATE OR REPLACE VIEW analytics.vw_product_performance AS
SELECT category,subcategory,product_name,SUM(quantity) FILTER(WHERE status='Completed') AS units_sold,
       SUM(net_sales) FILTER(WHERE status='Completed') AS revenue,
       SUM(profit) FILTER(WHERE status='Completed') AS profit
FROM analytics.vw_sales_enriched GROUP BY 1,2,3;

CREATE OR REPLACE VIEW analytics.vw_customer_performance AS
SELECT customer_id,customer_name,segment,customer_city,
       COUNT(DISTINCT order_id) FILTER(WHERE status='Completed') AS orders,
       SUM(net_sales) FILTER(WHERE status='Completed') AS revenue,
       SUM(profit) FILTER(WHERE status='Completed') AS profit,MAX(order_date) AS last_order_date
FROM analytics.vw_sales_enriched GROUP BY 1,2,3,4;
