import pandas as pd

def make_fact(orders: pd.DataFrame, items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    x=items.merge(orders,on="order_id",how="left",validate="many_to_one")
    x=x.merge(products[["product_id","unit_cost","category","subcategory"]],on="product_id",how="left",validate="many_to_one")
    if x.order_date.isna().any(): raise ValueError("Order item references an unknown order")
    if x.unit_cost.isna().any(): raise ValueError("Order item references an unknown product")
    x["gross_sales"]=x.quantity*x.unit_price
    x["net_sales"]=x.gross_sales*(1-x.discount_pct)
    x["total_cost"]=x.quantity*x.unit_cost
    x["profit"]=x.net_sales-x.total_cost
    x["order_date"]=pd.to_datetime(x.order_date).dt.date
    return x[["order_item_id","order_id","order_date","customer_id","product_id","region_id","sales_rep_id",
              "channel","status","quantity","unit_price","discount_pct","gross_sales","net_sales","total_cost","profit"]]
