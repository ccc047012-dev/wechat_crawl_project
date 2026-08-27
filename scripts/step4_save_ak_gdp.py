# -*- coding: utf-8 -*-
import akshare as ak, os
OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
os.makedirs(OUT, exist_ok=True)

try:
    gdp_cn = ak.macro_china_gdp()
    gdp_cn.to_csv(os.path.join(OUT, "akshare_China_GDP_quarterly.csv"), index=False, encoding="utf-8-sig")
    print(f"[ok] akshare_China_GDP_quarterly.csv rows={len(gdp_cn)}")
except Exception as e:
    print("china gdp fail:", e)

try:
    gdp_us = ak.macro_usa_gdp_monthly()
    gdp_us.to_csv(os.path.join(OUT, "akshare_USA_GDP_mom_monthly.csv"), index=False, encoding="utf-8-sig")
    print(f"[ok] akshare_USA_GDP_mom_monthly.csv rows={len(gdp_us)}")
except Exception as e:
    print("usa gdp mom fail:", e)
print("END")