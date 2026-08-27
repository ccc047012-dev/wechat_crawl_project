# -*- coding: utf-8 -*-
import akshare as ak, pandas as pd, os, traceback
OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
os.makedirs(OUT, exist_ok=True)

def save(df, name):
    if df is None or len(df)==0:
        print(f"[skip] {name} empty"); return
    p = os.path.join(OUT, name)
    df.to_csv(p, index=False, encoding="utf-8-sig")
    print(f"[ok] {name} rows={len(df)} -> {p}")
    print(df.head(3).to_string())

# 1. 美元人民币 日度 2015-2025
print("=== 1. 汇率 currency_boc_sina ===")
try:
    fx = ak.currency_boc_sina(symbol="美元", start_date="20150101", end_date="20251231")
    save(fx, "akshare_CNYUSD_daily_boc.csv")
except Exception as e:
    print("boc_sina fail:", e); traceback.print_exc()

print("=== 1b. 汇率 currency_history(USD->CNY) ===")
try:
    fx2 = ak.currency_history(base="USD", date="20240101", symbols="CNY")
    print(fx2.head(3).to_string())
except Exception as e:
    print("currency_history fail:", e)

# 2. 中国季度GDP
print("=== 2. 中国GDP macro_china_gdp ===")
try:
    gdp_cn = ak.macro_china_gdp()
    print(gdp_cn.head(3).to_string())
    print("cols:", list(gdp_cn.columns))
except Exception as e:
    print("macro_china_gdp fail:", e); traceback.print_exc()

# 3. 美国月度GDP
print("=== 3. 美国GDP macro_usa_gdp_monthly ===")
try:
    gdp_us = ak.macro_usa_gdp_monthly()
    print(gdp_us.head(3).to_string())
    print("cols:", list(gdp_us.columns))
except Exception as e:
    print("macro_usa_gdp_monthly fail:", e); traceback.print_exc()
print("SCRIPT END")