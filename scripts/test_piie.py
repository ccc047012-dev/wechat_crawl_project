import requests

# PIIE 贸易战关税数据 + NBER
urls = [
    ("PIIE trade war data page", "https://www.piie.com/sites/default/files/documents/2021-03/us-china-trade-war-tariff-data.csv"),
    ("PIIE 301 excel", "https://www.piie.com/sites/default/files/documents/us_china_tariff_timeline.xlsx"),
    ("USTR sec301 page", "https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions"),
]
for name, u in urls:
    try:
        r = requests.get(u, timeout=35, headers={"User-Agent":"Mozilla/5.0"})
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:50]}")
        print("  " + r.text[:250].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:80]}")
    print()