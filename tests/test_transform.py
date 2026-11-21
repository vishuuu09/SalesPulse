import pandas as pd
import pytest
from salespulse.transform import make_fact

def test_calculated_measures():
    orders=pd.DataFrame([{"order_id":"O1","order_date":"2025-01-01","customer_id":"C1","region_id":"R1","sales_rep_id":"S1","channel":"Online","status":"Completed"}])
    items=pd.DataFrame([{"order_item_id":"I1","order_id":"O1","product_id":"P1","quantity":2,"unit_price":100,"discount_pct":.1}])
    products=pd.DataFrame([{"product_id":"P1","unit_cost":60,"category":"Tech","subcategory":"Laptop"}])
    row=make_fact(orders,items,products).iloc[0]
    assert row.gross_sales==200 and row.net_sales==180 and row.profit==60

def test_unmatched_order_fails():
    orders=pd.DataFrame(columns=["order_id","order_date","customer_id","region_id","sales_rep_id","channel","status"])
    items=pd.DataFrame([{"order_item_id":"I1","order_id":"NO","product_id":"P1","quantity":1,"unit_price":10,"discount_pct":0}])
    products=pd.DataFrame([{"product_id":"P1","unit_cost":5,"category":"X","subcategory":"Y"}])
    with pytest.raises(ValueError): make_fact(orders,items,products)
