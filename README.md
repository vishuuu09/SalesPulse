# SalesPulse — Advanced Sales Analytics & BI Platform

A portfolio project demonstrating Python ETL, Pandas/NumPy, PostgreSQL, advanced SQL, data quality, dimensional modelling and Power BI reporting.

**Dataset:** included synthetic fictional retail data (5,000 orders). It is not real business data.

## Architecture
CSV source data → Python ETL + quality rules → PostgreSQL star schema → SQL analytics views → Power BI dashboards → business recommendations.

## Windows setup
1. Install Python 3.11+, Docker Desktop and (for dashboards) Power BI Desktop.
2. In PowerShell:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d db
```
3. Generate data (or use included files):
```powershell
python -m salespulse.cli generate --orders 5000
```
4. Run pipeline:
```powershell
python -m salespulse.cli run
```
5. Test:
```powershell
pytest -q
```
PostgreSQL: localhost:5432, database/user `salespulse`, password `salespulse_dev_password` (local demo only).

## Folder map
- `salespulse/`: configuration, generator, validation, transformation, database and orchestration.
- `sql/`: schema, analytics views and business analysis queries.
- `data/raw/`: six source CSVs.
- `data/processed/`: validated fact extract.
- `data/quarantine/`: rejected records with reason codes.
- `tests/`: unit tests.
- `docs/`: data dictionary, Power BI build guide and interview questions.

## Power BI pages
1. Executive Overview: revenue, profit, orders, AOV, margin, monthly trend.
2. Regional Performance: region/city revenue and profitability.
3. Product Analysis: category, subcategory and top product performance.
4. Customer Analytics: segment, top customers, repeat purchase patterns.

Connect Power BI to PostgreSQL and import `analytics.vw_sales_enriched` plus the aggregate views. DAX and visual guidance are in `docs/POWER_BI_GUIDE.md`.

## Quality and design
- One fact row = one order line. Use `COUNT(DISTINCT order_id)` for order counts.
- Invalid quantity, price, discount and duplicate line IDs are quarantined.
- Measures: gross sales = quantity × unit price; net sales = gross sales × (1 − discount); cost = quantity × unit cost; profit = net sales − cost.
- Fact load uses `ON CONFLICT(order_item_id)` for repeatable loads.
- This demo refreshes dimensions. For production, add SCD Type 2, incremental watermarks, orchestration, secrets management and monitoring.

## Honest resume guidance
Do not claim Power BI, Salesforce integration, dashboard impact or performance improvements until you have built, run and validated those components yourself. This project models CRM-style customer and sales-rep information but does not connect to Salesforce.
