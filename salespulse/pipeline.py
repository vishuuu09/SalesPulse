import logging
import pandas as pd
from sqlalchemy import text
from salespulse.config import settings
from salespulse.db import engine,run_sql_file
from salespulse.quality import validate_items
from salespulse.transform import make_fact

log=logging.getLogger("salespulse")

def read(name):
    path = settings.raw_dir / name

    if not path.exists():
        raise FileNotFoundError(f"{path} not found; run generate first")

    if name in ["customers.csv", "orders.csv"]:
        return pd.read_csv(path, parse_dates=["signup_date"] if name == "customers.csv" else ["order_date"])

    return pd.read_csv(path)

def run():
    settings.processed_dir.mkdir(parents=True,exist_ok=True)
    settings.quarantine_dir.mkdir(parents=True,exist_ok=True)
    customers,products,regions,reps,orders,items=[read(n) for n in
        ["customers.csv","products.csv","regions.csv","sales_reps.csv","orders.csv","order_items.csv"]]
    q=validate_items(items)
    q.rejected.to_csv(settings.quarantine_dir/"rejected_order_items.csv",index=False)
    fact=make_fact(orders,q.accepted,products)
    fact.to_csv(settings.processed_dir/"fact_sales_ready.csv",index=False)
    db=engine()
    run_sql_file(db,"sql/01_schema.sql")
    # Refresh dimensions for this demo. Production history tracking would use SCD Type 2.
    with db.begin() as conn:
        for table,df in [("dim_customer",customers),("dim_product",products),("dim_region",regions),("dim_sales_rep",reps)]:
            conn.execute(text(f"TRUNCATE warehouse.{table} CASCADE"))
            df.to_sql(table,conn,schema="warehouse",if_exists="append",index=False,method="multi",chunksize=1000)
    fact.to_sql("fact_stage",db,schema="warehouse",if_exists="replace",index=False,method="multi",chunksize=1000)
    with db.begin() as conn:
        conn.execute(text("""
        INSERT INTO warehouse.fact_sales
        SELECT order_item_id,order_id,order_date,customer_id,product_id,region_id,sales_rep_id,channel,status,
               quantity,unit_price,discount_pct,gross_sales,net_sales,total_cost,profit
        FROM warehouse.fact_stage
        ON CONFLICT(order_item_id) DO UPDATE SET
          order_id=EXCLUDED.order_id,order_date=EXCLUDED.order_date,customer_id=EXCLUDED.customer_id,
          product_id=EXCLUDED.product_id,region_id=EXCLUDED.region_id,sales_rep_id=EXCLUDED.sales_rep_id,
          channel=EXCLUDED.channel,status=EXCLUDED.status,quantity=EXCLUDED.quantity,unit_price=EXCLUDED.unit_price,
          discount_pct=EXCLUDED.discount_pct,gross_sales=EXCLUDED.gross_sales,net_sales=EXCLUDED.net_sales,
          total_cost=EXCLUDED.total_cost,profit=EXCLUDED.profit;
        DROP TABLE warehouse.fact_stage;
        """))
    run_sql_file(db,"sql/02_views.sql")
    result={**q.metrics,"fact_rows_loaded":len(fact)}
    log.info("ETL completed: %s",result)
    return result
