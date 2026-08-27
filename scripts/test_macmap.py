import requests

# 美国MFN关税公开副本源
urls = [
    ("Macmap USA MFN", "https://www.macmap.org/api/results/custom/query?reporter=842&partner=all&product=61-64&year=2020"),
    ("Macmap root", "https://www.macmap.org/"),
    ("Trade gov tariff tool", "https://www.trade.gov/machinery-equipment-tariffs"),
    ("Census foreign trade schedule b search", "https://uscensus.prod.3ceonline.com/"),
]
for name, u in urls:
    try:
        r = requests.get(u, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} ct={r.headers.get('Content-Type','')[:40]} len={len(r.content)}")
        print("  "+r.text[:220].replace(chr(10)," "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")