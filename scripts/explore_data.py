# -*- coding: utf-8 -*-
import pandas as pd, os, glob

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"

# 读取汇率日度数据
fx = pd.read_csv(os.path.join(OUT, "akshare_CNYUSD_daily_boc.csv"))
print("汇率数据 shape:", fx.shape)
print(fx.head(3).to_string())
print("列名:", list(fx.columns))
print("日期范围:", fx["日期"].min(), "-", fx["日期"].max())

# 中国GDP季度
for f in glob.glob(os.path.join(OUT, "akshare_China_GDP*.csv")):
    gdp = pd.read_csv(f)
    print(f"\n中国GDP {os.path.basename(f)} shape={gdp.shape}")
    print(gdp.head(3).to_string())

# 美国GDP BEA是Excel，先检查文件存在
bea = os.path.join(OUT, "BEA_NIPA_Section1All.xlsx")
print("\nBEA文件大小:", os.path.getsize(bea))