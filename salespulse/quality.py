from dataclasses import dataclass
import pandas as pd

REQUIRED={"order_item_id","order_id","product_id","quantity","unit_price","discount_pct"}

@dataclass
class QualityResult:
    accepted: pd.DataFrame
    rejected: pd.DataFrame
    metrics: dict

def validate_items(df: pd.DataFrame) -> QualityResult:
    missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {sorted(missing)}")
    x=df.copy()
    for c in ["quantity","unit_price","discount_pct"]:
        x[c]=pd.to_numeric(x[c],errors="coerce")
    reason=pd.Series("",index=x.index,dtype="object")
    checks=[
        (x[["order_item_id","order_id","product_id"]].isna().any(axis=1),"missing_key"),
        (x.order_item_id.duplicated(keep=False),"duplicate_order_item_id"),
        (x.quantity.isna() | (x.quantity<=0),"invalid_quantity"),
        (x.unit_price.isna() | (x.unit_price<0),"invalid_unit_price"),
        (x.discount_pct.isna() | (x.discount_pct<0) | (x.discount_pct>1),"invalid_discount")]
    for mask,label in checks:
        reason.loc[mask]=reason.loc[mask].apply(lambda s: f"{s};{label}" if s else label)
    bad=reason.ne("")
    rejected=x.loc[bad].copy()
    rejected["rejection_reason"]=reason.loc[bad]
    metrics={"input_rows":len(x),"accepted_rows":int((~bad).sum()),"rejected_rows":int(bad.sum()),
             "duplicate_ids":int(x.order_item_id.duplicated(keep=False).sum())}
    return QualityResult(x.loc[~bad].copy(),rejected,metrics)
