# -*- coding: utf-8 -*-
import requests, csv, os

OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
os.makedirs(OUT, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def fetch_wb(code, indicator, fname):
    url = f"https://api.worldbank.org/v2/country/{code}/indicator/{indicator}"
    params = {"format": "json", "per_page": 100}
    try:
        r = requests.get(url, params=params, headers=H, timeout=60)
        print(f"[{code}/{indicator}] HTTP {r.status_code}", flush=True)
        if r.status_code != 200:
            print("   -> non200: " + r.text[:200], flush=True)
            return False
        data = r.json()
        if len(data) < 2 or data[1] is None:
            print("   -> empty", flush=True)
            return False
        rows = []
        for rec in data[1]:
            if rec.get("value") is not None:
                rows.append({
                    "国家代码": rec["country"]["id"],
                    "国家": rec["country"]["value"],
                    "指标代码": rec["indicator"]["id"],
                    "指标名称": rec["indicator"]["value"],
                    "年份": rec["date"],
                    "数值": rec["value"],
                })
        path = os.path.join(OUT, fname)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"   -> OK {len(rows)} rows -> {path}", flush=True)
        return True
    except Exception as e:
        print(f"   -> FAIL {type(e).__name__}: {e}", flush=True)
        return False

jobs = [
    ("CHN", "NY.GDP.MKTP.CD", "WB_China_GDP_currentUSD_annual.csv"),
    ("USA", "NY.GDP.MKTP.CD", "WB_USA_GDP_currentUSD_annual.csv"),
    ("CHN", "NY.GDP.MKTP.KN", "WB_China_GDP_constantLCU_annual.csv"),
    ("USA", "NY.GDP.MKTP.KN", "WB_USA_GDP_constantLCU_annual.csv"),
]
ok = 0
for c, i, f in jobs:
    if fetch_wb(c, i, f):
        ok += 1
print(f"\nDONE {ok}/{len(jobs)} success")