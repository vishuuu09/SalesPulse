from salespulse.quality import validate_items

def test_valid_rows(items):
    result=validate_items(items)
    assert len(result.accepted)==2 and len(result.rejected)==0

def test_invalid_quantity_quarantined(items):
    items.loc[0,"quantity"]=0
    result=validate_items(items)
    assert len(result.rejected)==1
    assert "invalid_quantity" in result.rejected.iloc[0].rejection_reason

def test_duplicate_keys_rejected(items):
    items.loc[1,"order_item_id"]="I1"
    assert len(validate_items(items).rejected)==2
