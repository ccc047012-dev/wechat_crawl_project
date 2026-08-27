# -*- coding: utf-8 -*-
import pandas as pd, os
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "raw_data"
PROC = BASE / "processed_data"
os.makedirs(PROC, exist_ok=True)

# 1. 汇率月度均值
src_fx = OUT / "akshare_CNYUSD_daily_boc.csv"
if src_fx.exists():
    dfx = pd.read_csv(src_fx)
    dfx["日期"] = pd.to_datetime(dfx["日期"])
    dfx["YearMonth"] = dfx["日期"].dt.strftime("%Y%m")
    fx_month = dfx.groupby("YearMonth")["央行中间价"].mean().reset_index()
    fx_month.columns = ["YearMonth", "CNY_per_USD"]
    fx_month["CNY_per_USD"] = fx_month["CNY_per_USD"] / 100
    fx_month.to_csv(PROC / "processed_exchange_rate_monthly.csv", index=False, encoding="utf-8-sig")
    print("汇率月度:", fx_month.shape)
    print(fx_month.head(3).to_string())
    print(fx_month.tail(3).to_string())

# 2. 中国GDP季度标准化
src_cn = OUT / "akshare_China_GDP_quarterly.csv"
if src_cn.exists():
    df_cn = pd.read_csv(src_cn)
    col_map = {c: c.replace("-","").replace(" ","") for c in df_cn.columns}
    df_cn = df_cn.rename(columns=col_map)
    print("\n中国GDP列名:", list(df_cn.columns))
    df_cn.to_csv(PROC / "processed_China_GDP_quarterly.csv", index=False, encoding="utf-8-sig")
    print("中国GDP季度保存完成,", df_cn.shape)
    print(df_cn.head(3).to_string())