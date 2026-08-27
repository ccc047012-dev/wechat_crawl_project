import requests
# UNCTAD TRAINS 关税数据 API
tests = [
    ("TRAINS proj", "https://trains.unctad.org/api/v1/tariff?reporter=840,842&partner=156&product=42&year=2020"),
    ("UNCTAD stat", "https://unctadstat-api.unctad.org/bulkdownload/UNCTAD_TRAINS_CIF_USD/UNCTAD_TRAINS_CIF_USD_full.zip"),
    ("unctadstat index", "https://unctadstat-api.unctad.org/bulkdownload/UNCTAD_TRAINS_CIF_USD/"),
]
for name, u in tests:
    try:
        r = requests.get(u, timeout=20)
        print(f"{name}: HTTP {r.status_code} len={len(r.content)} ct={r.headers.get('Content-Type','')[:40]}")
        print("  " + r.text[:150].replace(chr(10), " "))
    except Exception as e:
        print(f"{name}: FAIL {type(e).__name__}: {str(e)[:70]}")