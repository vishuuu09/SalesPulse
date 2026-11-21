from pathlib import Path
import numpy as np
import pandas as pd

def generate(output: Path, n_orders: int = 5000, seed: int = 42):
    rng = np.random.default_rng(seed)
    output.mkdir(parents=True, exist_ok=True)
    n_cust, n_prod, n_rep = max(500, n_orders // 3), 60, 24
    customers = pd.DataFrame({
        "customer_id":[f"C{i:05}" for i in range(1,n_cust+1)],
        "customer_name":[f"Customer {i:04}" for i in range(1,n_cust+1)],
        "segment":rng.choice(["Consumer","Corporate","Small Business"],n_cust,p=[.58,.27,.15]),
        "city":rng.choice(["Hyderabad","Bengaluru","Mumbai","Delhi","Pune","Chennai","Kolkata"],n_cust),
        "signup_date":pd.Timestamp("2021-01-01")+pd.to_timedelta(rng.integers(0,1500,n_cust),unit="D")})
    cats = {"Technology":["Laptop","Monitor","Keyboard","Mouse","Headphones"],
            "Furniture":["Desk","Chair","Bookshelf","Cabinet"],
            "Office Supplies":["Notebook","Pen Set","Paper","Stapler"]}
    prows=[]
    for i in range(1,n_prod+1):
        cat=list(cats)[(i-1)%3]; sub=cats[cat][(i-1)%len(cats[cat])]
        prows.append({"product_id":f"P{i:04}","product_name":f"{sub} Model {i:02}",
                      "category":cat,"subcategory":sub,"unit_cost":round(float(rng.uniform(8,650)),2),
                      "list_price":round(float(rng.uniform(15,1000)),2)})
    products=pd.DataFrame(prows)
    region_pairs=[("North","Delhi"),("South","Bengaluru"),("South","Chennai"),("West","Mumbai"),("West","Pune"),("East","Kolkata")]
    regions=pd.DataFrame([{"region_id":f"R{i+1:02}","region_name":r,"city":c} for i,(r,c) in enumerate(region_pairs)])
    reps=pd.DataFrame({"sales_rep_id":[f"SR{i:03}" for i in range(1,n_rep+1)],
                       "sales_rep_name":[f"Sales Representative {i:02}" for i in range(1,n_rep+1)],
                       "team":rng.choice(["Enterprise","Retail","SMB"],n_rep)})
    o_rows=[]; i_rows=[]; line=1
    for i in range(n_orders):
        oid=f"O{i+1:07}"; cust=customers.iloc[int(rng.integers(n_cust))]
        reg=regions.iloc[int(rng.integers(len(regions)))]; rep=reps.iloc[int(rng.integers(n_rep))]
        o_rows.append({"order_id":oid,"order_date":pd.Timestamp("2023-01-01")+pd.Timedelta(days=int(rng.integers(1095))),
                       "customer_id":cust.customer_id,"region_id":reg.region_id,"sales_rep_id":rep.sales_rep_id,
                       "channel":rng.choice(["Online","Retail","Partner"],p=[.48,.37,.15]),
                       "status":rng.choice(["Completed","Returned","Cancelled"],p=[.94,.04,.02])})
        for _ in range(int(rng.integers(1,5))):
            p=products.iloc[int(rng.integers(n_prod))]
            i_rows.append({"order_item_id":f"OI{line:09}","order_id":oid,"product_id":p.product_id,
                           "quantity":int(rng.integers(1,6)),
                           "unit_price":round(float(p.list_price)*float(rng.uniform(.92,1.08)),2),
                           "discount_pct":float(rng.choice([0,.05,.10,.15,.20],p=[.45,.20,.18,.12,.05]))})
            line+=1
    items=pd.DataFrame(i_rows)
    # Deliberate sample defects to exercise quarantine logic.
    items.loc[0,"quantity"]=0; items.loc[1,"discount_pct"]=1.5; items.loc[2,"unit_price"]=-10
    for name, frame in {"customers.csv":customers,"products.csv":products,"regions.csv":regions,
                        "sales_reps.csv":reps,"orders.csv":pd.DataFrame(o_rows),"order_items.csv":items}.items():
        frame.to_csv(output/name,index=False)
