-- Top products
SELECT product_name,SUM(net_sales) revenue FROM analytics.vw_sales_enriched
WHERE status='Completed' GROUP BY product_name ORDER BY revenue DESC LIMIT 10;

-- Month-over-month growth
WITH m AS (SELECT date_trunc('month',order_date)::date month,
                  SUM(net_sales) FILTER(WHERE status='Completed') revenue
           FROM analytics.vw_sales_enriched GROUP BY 1)
SELECT month,revenue,LAG(revenue) OVER(ORDER BY month) previous_month,
       ROUND(100*(revenue-LAG(revenue) OVER(ORDER BY month))/
       NULLIF(LAG(revenue) OVER(ORDER BY month),0),2) mom_growth_pct FROM m ORDER BY month;

-- Rank representatives inside each region
WITH r AS (SELECT region_name,sales_rep_name,
                  SUM(net_sales) FILTER(WHERE status='Completed') revenue
           FROM analytics.vw_sales_enriched GROUP BY 1,2)
SELECT *,DENSE_RANK() OVER(PARTITION BY region_name ORDER BY revenue DESC) regional_rank FROM r;

-- Customer repeat behaviour
SELECT customer_id,COUNT(DISTINCT order_id) order_count,
       CASE WHEN COUNT(DISTINCT order_id)>=5 THEN 'Frequent'
            WHEN COUNT(DISTINCT order_id)>=2 THEN 'Repeat' ELSE 'One-time' END customer_type
FROM analytics.vw_sales_enriched WHERE status='Completed' GROUP BY customer_id;

-- Return rate by channel
SELECT channel,COUNT(DISTINCT order_id) total_orders,
       COUNT(DISTINCT order_id) FILTER(WHERE status='Returned') returned_orders,
       ROUND(100.0*COUNT(DISTINCT order_id) FILTER(WHERE status='Returned')/
       NULLIF(COUNT(DISTINCT order_id),0),2) return_rate_pct
FROM analytics.vw_sales_enriched GROUP BY channel;
