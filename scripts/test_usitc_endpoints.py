import requests

# USITC 官方对公众端点探索
base = "https://dataweb.usitc.gov"
tests = [
    base + "/DataWebApi/api/Data",
    base + "/api/data",
    base + "/api/v1/data",
    base + "/api/reports",
]
for u in tests:
    try:
        r = requests.get(u, timeout=15)
        ct = r.headers.get("Content-Type", "")
        print(f"{u}")
        print(f"  HTTP {r.status_code} Content-Type={ct} len={len(r.content)}")
        print("  " + r.text[:120].replace(chr(10), " "))
    except Exception as e:
        print(f"{u} FAIL {type(e).__name__}: {str(e)[:60]}")