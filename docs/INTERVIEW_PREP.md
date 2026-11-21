# Interview preparation
1. Why use a star schema? It separates measurable transactions from descriptive dimensions and simplifies BI queries.
2. Why COUNT(DISTINCT order_id)? Fact grain is order item, so an order may have multiple rows.
3. What does LAG do? Accesses a prior row in an ordered window, useful for month-over-month comparisons.
4. How are invalid records handled? Quarantine with explicit reason codes and report accepted/rejected counts.
5. What is ETL? Extract source data, transform/validate it, then load into a target.
6. How would you productionize? Incremental loads, SCD Type 2, orchestration, secrets, CI/CD, monitoring and reconciliation.
7. Does this connect to Salesforce? No. It uses CRM-like customer and rep entities but does not implement Salesforce integration.
