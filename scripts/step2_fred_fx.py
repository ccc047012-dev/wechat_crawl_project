# -*- coding: utf-8 -*-
import requests, os
OUT = r"C:\Users\26936\wechat_crawl_project\raw_data"
os.makedirs(OUT, exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 1) FRED DEXCHUS (日度，人民币/美元)
urls = {
    "FRED_DEXCHUS_CNYUSD_daily.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCHUS",
    "FRED_DEXCHUS_CNYUSD_daily_2.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DEXCHUS&scale=left&cosd=2015-01-01&coed=2025-12-31&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2026-01-01&revision_date=2026-01-01&nd=2015-01-01",
}
for fname, url in urls.items():
    try:
        r = requests.get(url, headers=H, timeout=30)
        print(f"[{fname}] HTTP {r.status_code} len={len(r.content)}", flush=True)
        if r.status_code == 200 and len(r.content) > 50:
            path = os.path.join(OUT, fname)
            open(path, "wb").write(r.content)
            print("   -> OK", flush=True)
            print(r.content[:120].decode("utf-8", "replace"), flush=True)
            break
        else:
            print("   -> bad", flush=True)
    except Exception as e:
        print(f"   -> FAIL {type(e).__name__}: {e}", flush=True)
print("DONE")