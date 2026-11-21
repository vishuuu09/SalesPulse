CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE TABLE IF NOT EXISTS warehouse.dim_customer(
 customer_id TEXT PRIMARY KEY, customer_name TEXT NOT NULL, segment TEXT, city TEXT, signup_date DATE);
CREATE TABLE IF NOT EXISTS warehouse.dim_product(
 product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT, subcategory TEXT, unit_cost NUMERIC(12,2), list_price NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS warehouse.dim_region(
 region_id TEXT PRIMARY KEY, region_name TEXT NOT NULL, city TEXT);
CREATE TABLE IF NOT EXISTS warehouse.dim_sales_rep(
 sales_rep_id TEXT PRIMARY KEY, sales_rep_name TEXT NOT NULL, team TEXT);
CREATE TABLE IF NOT EXISTS warehouse.fact_sales(
 order_item_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, order_date DATE NOT NULL,
 customer_id TEXT NOT NULL REFERENCES warehouse.dim_customer(customer_id),
 product_id TEXT NOT NULL REFERENCES warehouse.dim_product(product_id),
 region_id TEXT NOT NULL REFERENCES warehouse.dim_region(region_id),
 sales_rep_id TEXT NOT NULL REFERENCES warehouse.dim_sales_rep(sales_rep_id),
 channel TEXT,status TEXT,quantity INTEGER NOT NULL CHECK(quantity>0),
 unit_price NUMERIC(12,2) NOT NULL CHECK(unit_price>=0),
 discount_pct NUMERIC(5,4) NOT NULL CHECK(discount_pct BETWEEN 0 AND 1),
 gross_sales NUMERIC(14,2),net_sales NUMERIC(14,2),total_cost NUMERIC(14,2),profit NUMERIC(14,2));
CREATE INDEX IF NOT EXISTS ix_fact_date ON warehouse.fact_sales(order_date);
CREATE INDEX IF NOT EXISTS ix_fact_customer ON warehouse.fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS ix_fact_product ON warehouse.fact_sales(product_id);
