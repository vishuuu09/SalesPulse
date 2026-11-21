import pandas as pd
import pytest

@pytest.fixture
def items():
    return pd.DataFrame([
      {"order_item_id":"I1","order_id":"O1","product_id":"P1","quantity":2,"unit_price":100,"discount_pct":.1},
      {"order_item_id":"I2","order_id":"O2","product_id":"P2","quantity":1,"unit_price":50,"discount_pct":0}])
